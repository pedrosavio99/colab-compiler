def generate_python(ast):
    python_code = []
    python_code.append("class Signal:\n    def __init__(self, value=0, bit_width=None):\n        self.value = value\n        self.bit_width = bit_width\n        if bit_width:\n            self.max_value = (1 << (bit_width[0] - bit_width[1] + 1)) - 1\n\n    def set_value(self, value):\n        if self.bit_width:\n            self.value = value & self.max_value\n        else:\n            self.value = value\n\n")

    for node in ast['body']:
        if node['type'] == 'Module':
            module_name = node['name']
            ports = node['ports']
            body = node['body']

            # Definir a classe do módulo
            python_code.append(f"class {module_name}:")
            python_code.append("    def __init__(self):")

            # Inicializar portas como sinais
            for port in ports:
                port_name = port['name']
                bit_width = port.get('bit_width')
                data_type = port.get('data_type', '')
                comment = f"{port['type']}"
                if data_type:
                    comment += f", {data_type}"
                if bit_width:
                    comment += f", [{bit_width[0]}:{bit_width[1]}]"
                python_code.append(f"        self.{port_name} = Signal(bit_width={bit_width})  # {comment}")

            # Inicializar variáveis internas (wire, reg)
            for stmt in body:
                if stmt['type'] == 'Declaration':
                    var_name = stmt['name']
                    bit_width = stmt.get('bit_width')
                    python_code.append(f"        self.{var_name} = Signal(bit_width={bit_width})  # {stmt['decl_type']}")

            # Método para atualizar lógica combinacional
            python_code.append("\n    def update_combinational(self):")
            combinational_found = False
            for stmt in body:
                if stmt['type'] == 'Assign':
                    lhs = stmt['lhs']
                    rhs = translate_expression(stmt['rhs'])
                    python_code.append(f"        self.{lhs}.set_value({rhs})")
                    combinational_found = True
            if not combinational_found:
                python_code.append("        pass")

            # Método para simular lógica sequencial
            python_code.append("\n    def update_sequential(self):")
            sequential_found = False
            for stmt in body:
                if stmt['type'] == 'Always':
                    sensitivity_list = stmt['sensitivity_list']
                    statements = stmt['statements']
                    # Adicionar comentário sobre a lista de sensibilidade
                    sensitivity_comment = "        # Sensível a " + ", ".join(
                        f"{s['edge']} de {s['signal']}" if s['edge'] else s['signal'] 
                        for s in sensitivity_list
                    )
                    python_code.append(sensitivity_comment)
                    python_code.append("        # Simulação simplificada: atualiza na borda")
                    # Gerar as instruções apenas uma vez
                    for sub_stmt in statements:
                        python_code.append(translate_statement(sub_stmt, indent=2))
                    sequential_found = True
            if not sequential_found:
                python_code.append("        pass")

            # Método principal para executar o módulo
            python_code.append("\n    def run(self):")
            python_code.append("        self.update_combinational()")
            python_code.append("        self.update_sequential()")

    return "\n".join(python_code)

def translate_expression(expr):
    result = []
    for token_type, token_value in expr:
        if token_type == 'IDENTIFIER':
            result.append(f"self.{token_value}.value")
        elif token_type == 'NUMBER':
            if "'b" in token_value:
                bits, value = token_value.split("'b")
                result.append(str(int(value, 2)))
            elif "'h" in token_value:
                bits, value = token_value.split("'h")
                result.append(str(int(value, 16)))
            else:
                result.append(token_value)
        elif token_type == 'OPERATOR':
            if token_value == '&&':
                result.append('and')
            elif token_value == '||':
                result.append('or')
            elif token_value == '!':
                result.append('not ')
            elif token_value == '&':
                result.append('&')
            elif token_value == '|':
                result.append('|')
            elif token_value == '^':
                result.append('^')
            else:
                result.append(token_value)
        elif token_type == 'SYMBOL':
            result.append(token_value)
    return ' '.join(result)

def translate_statement(stmt, indent=0):
    indent_str = "    " * indent
    if stmt['type'] == 'Assignment':
        lhs = stmt['lhs']
        rhs = translate_expression(stmt['rhs'])
        return f"{indent_str}self.{lhs}.set_value({rhs})"
    elif stmt['type'] == 'If':
        condition = translate_expression(stmt['condition'])
        true_code = [translate_statement(s, indent + 1) for s in stmt['true_statements']]
        false_code = [translate_statement(s, indent + 1) for s in stmt['false_statements']]
        code = [f"{indent_str}if {condition}:"]
        code.extend(true_code)
        if false_code:
            code.append(f"{indent_str}else:")
            code.extend(false_code)
        return "\n".join(code)
    return f"{indent_str}pass  # Declaração não suportada: {stmt['type']}"