def generate_python(ast):
    print("Iniciando geração de código Python com AST:", ast)
    python_code = []
    python_code.append("class Signal:\n    def __init__(self, value=0, bit_width=None):\n        self.value = value\n        self.bit_width = bit_width\n        if bit_width:\n            self.max_value = (1 << (bit_width[0] - bit_width[1] + 1)) - 1\n\n    def set_value(self, value):\n        if self.bit_width:\n            self.value = value & self.max_value\n        else:\n            self.value = value\n\n")

    for node in ast['body']:
        if node['type'] == 'Module':
            module_name = node['name']
            ports = node['ports']
            body = node['body']

            python_code.append(f"class {module_name}:")
            python_code.append("    def __init__(self):")
            print(f"Gerando __init__ para módulo {module_name}")

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
                print(f"Adicionado porto: self.{port_name}")

            for stmt in body:
                if stmt['type'] == 'Declaration':
                    var_name = stmt['name']
                    bit_width = stmt.get('bit_width')
                    initial_value = stmt.get('initial_value')
                    value_str = f", value={initial_value}" if initial_value is not None else ""
                    python_code.append(f"        self.{var_name} = Signal(bit_width={bit_width}{value_str})  # {stmt['decl_type']}")
                    print(f"Adicionada declaração: self.{var_name}")

            python_code.append("        self.time = 0  # Simulação de $time")

            python_code.append("\n    def update_combinational(self):")
            combinational_found = False
            for stmt in body:
                if stmt['type'] == 'Assign':
                    lhs = stmt['lhs']
                    rhs = translate_expression(stmt['rhs'])
                    python_code.append(f"        self.{lhs}.set_value({rhs})")
                    print(f"Adicionada atribuição combinacional: self.{lhs}.set_value({rhs})")
                    combinational_found = True
            if not combinational_found:
                python_code.append("        pass")

            python_code.append("\n    def update_sequential(self):")
            sequential_found = False
            for stmt in body:
                if stmt['type'] == 'Always':
                    sensitivity_list = stmt['sensitivity_list']
                    statements = stmt['statements']
                    sensitivity_comment = "        # Sensível a " + ", ".join(
                        f"{s['edge']} de {s['signal']}" if s['edge'] else s['signal'] 
                        for s in sensitivity_list
                    )
                    python_code.append(sensitivity_comment)
                    python_code.append("        # Simulação simplificada: atualiza na borda")
                    for sub_stmt in statements:
                        python_code.append(translate_statement(sub_stmt, indent=2))
                    print(f"Adicionado bloco always: {sensitivity_list}")
                    sequential_found = True
                elif stmt['type'] == 'AlwaysDelay':
                    python_code.append(f"        # Clock gerado com atraso de {stmt['delay']} unidades")
                    python_code.append(f"        # Simulação simplificada: alterna o sinal")
                    python_code.append(translate_statement(stmt['statement'], indent=2))
                    print(f"Adicionado AlwaysDelay com delay {stmt['delay']}")
                    sequential_found = True
            if not sequential_found:
                python_code.append("        pass")

            has_initial = False
            for stmt in body:
                if stmt['type'] == 'Initial':
                    python_code.append("\n    def run_initial(self):")
                    python_code.append("        # Simulação do bloco initial")
                    for sub_stmt in stmt['statements']:
                        if sub_stmt['type'] == 'Monitor':
                            format_string = sub_stmt['args'][0]['value']
                            format_string = format_string.replace('%t', '{self.time}').replace('%d', '{self.count.value}')
                            python_code.append(f"        print(f\"{format_string}\")")
                        elif sub_stmt['type'] == 'DelayAssignment':
                            python_code.append(f"        if self.time == {sub_stmt['delay']}:")
                            python_code.append(f"            self.{sub_stmt['lhs']}.set_value({translate_expression(sub_stmt['rhs'])})")
                        elif sub_stmt['type'] == 'Finish':
                            python_code.append(f"        if self.time == {sub_stmt['delay']}:")
                            python_code.append("            return False  # $finish")
                    python_code.append("        return True")
                    has_initial = True
                    break

            python_code.append("\n    def run(self):")
            if has_initial:
                python_code.append("        while self.run_initial():")
                python_code.append("            self.update_combinational()")
                python_code.append("            self.update_sequential()")
                for stmt in body:
                    if stmt['type'] == 'AlwaysDelay':
                        python_code.append(f"            self.time += {stmt['delay']}")
                        break
                else:
                    python_code.append("            self.time += 1  # Default time step")
            else:
                python_code.append("        self.update_combinational()")
                python_code.append("        self.update_sequential()")

            # Adicionando o bloco de teste manual apenas uma vez
            python_code.append("\n# Teste manual")
            python_code.append("if __name__ == \"__main__\":")
            python_code.append(f"    sim = {module_name}()")
            python_code.append("    sim.run()")

    result = "\n".join(python_code)
    print("Código Python gerado:", result)
    return result

def translate_expression(expr):
    print(f"Traduzindo expressão: {expr}")
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
            elif token_value == '~':
                result.append('~')
            else:
                result.append(token_value)
        elif token_type == 'SYMBOL':
            result.append(token_value)
        elif token_type == 'STRING':
            result.append(f"'{token_value}'")
    translated = ' '.join(result)
    print(f"Expressão traduzida: {translated}")
    return translated

def translate_statement(stmt, indent=0):
    print(f"Traduzindo statement: {stmt}")
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