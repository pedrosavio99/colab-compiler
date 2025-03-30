def generate_python(ast):
    print("Iniciando geração de código Python com AST:", ast)
    python_code = []
    python_code.append("class Signal:\n    def __init__(self, value=0, bit_width=None):\n        self.value = value\n        self.bit_width = bit_width\n        if bit_width:\n            self.max_value = (1 << (bit_width[0] - bit_width[1] + 1)) - 1\n        self.prev_value = value  # Para detectar bordas\n\n    def set_value(self, value):\n        if self.bit_width:\n            self.value = value & self.max_value\n        else:\n            self.value = value\n\n")

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
            clock_delay = None
            for stmt in body:
                if stmt['type'] == 'AlwaysDelay':
                    clock_delay = stmt['delay']
                    python_code.append(f"        # Clock gerado com atraso de {stmt['delay']} unidades")
                    python_code.append(f"        # Simulação simplificada: alterna o sinal")
                    python_code.append(translate_statement(stmt['statement'], indent=2))
                    print(f"Adicionado AlwaysDelay com delay {stmt['delay']}")
                    sequential_found = True
                elif stmt['type'] == 'Always':
                    sensitivity_list = stmt['sensitivity_list']
                    statements = stmt['statements']
                    sensitivity_comment = "        # Sensível a " + ", ".join(
                        f"{s['edge']} de {s['signal']}" if s['edge'] else s['signal'] 
                        for s in sensitivity_list
                    )
                    python_code.append(sensitivity_comment)
                    python_code.append("        # Simulação simplificada: atualiza na borda")
                    conditions = []
                    for s in sensitivity_list:
                        if s['edge'] == 'posedge':
                            signal = s['signal']
                            conditions.append(f"self.{signal}.value and not self.{signal}.prev_value")
                    if conditions:
                        python_code.append(f"        if {' or '.join(conditions)}:  # Borda positiva")
                        for sub_stmt in statements:
                            python_code.append(translate_statement(sub_stmt, indent=3))
                        for s in sensitivity_list:
                            if s['edge'] == 'posedge':
                                signal = s['signal']
                                python_code.append(f"        self.{signal}.prev_value = self.{signal}.value")
                    else:
                        for sub_stmt in statements:
                            python_code.append(translate_statement(sub_stmt, indent=2))
                    print(f"Adicionado bloco always: {sensitivity_list}")
                    sequential_found = True
            if not sequential_found:
                python_code.append("        pass")

            has_initial = False
            total_delay = 0
            for stmt in body:
                if stmt['type'] == 'Initial':
                    python_code.append("\n    def run_initial(self):")
                    python_code.append("        # Simulação do bloco initial")
                    for sub_stmt in stmt['statements']:
                        if sub_stmt['type'] == 'Monitor':
                            format_string = sub_stmt['args'][0]['value']
                            specifiers = [part for part in format_string.split() if part in ('%t', '%b', '%d')]
                            args = []
                            if len(sub_stmt['args']) > 1:
                                if '%t' in format_string:
                                    args.append("self.time")
                                for arg in sub_stmt['args'][1]['value']:
                                    if arg[0] == 'IDENTIFIER':
                                        args.append(f"self.{arg[1]}.value")
                                    elif arg[0] == 'KEYWORD' and arg[1] == '$time':
                                        args.append("self.time")
                                    else:
                                        args.append(translate_expression([arg]))
                            new_format_string = format_string
                            for i, spec in enumerate(specifiers):
                                if i < len(args):
                                    if spec == '%t':
                                        new_format_string = new_format_string.replace('%t', '{self.time}', 1)
                                    elif spec == '%b':
                                        new_format_string = new_format_string.replace('%b', f'{{{args[i]}:b}}', 1)
                                    elif spec == '%d':
                                        new_format_string = new_format_string.replace('%d', f'{{{args[i]}}}', 1)
                            python_code.append(f"        print(f\"{new_format_string}\")")
                        elif sub_stmt['type'] == 'DelayAssignment':
                            total_delay += sub_stmt['delay']
                            python_code.append(f"        if self.time == {total_delay}:")
                            python_code.append(f"            self.{sub_stmt['lhs']}.set_value({translate_expression(sub_stmt['rhs'])})")
                        elif sub_stmt['type'] == 'Finish':
                            total_delay += sub_stmt['delay']
                            python_code.append(f"        if self.time == {total_delay}:")
                            python_code.append("            return False  # $finish")
                    python_code.append("        return True")
                    has_initial = True
                    break

            python_code.append("\n    def run(self):")
            if has_initial:
                python_code.append("        while self.run_initial():")
                python_code.append("            self.update_combinational()")
                python_code.append("            self.update_sequential()")
                time_step = clock_delay if clock_delay is not None else 1
                python_code.append(f"            self.time += {time_step}  # Passo de tempo baseado no clock")
            else:
                python_code.append("        self.update_combinational()")
                python_code.append("        self.update_sequential()")

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
    i = 0
    while i < len(expr):
        token_type, token_value = expr[i]
        
        if token_type == 'OPERATOR' and token_value == '~':
            i += 1
            if i < len(expr) and expr[i][0] == 'IDENTIFIER':
                result.append(f"1 - self.{expr[i][1]}.value")
                i += 1
            else:
                result.append('~')
        elif token_type == 'IDENTIFIER':
            result.append(f"self.{token_value}.value")
            i += 1
        elif token_type == 'NUMBER':
            if "'b" in token_value:
                bits, value = token_value.split("'b")
                result.append(str(int(value, 2)))
            elif "'h" in token_value:
                bits, value = token_value.split("'h")
                result.append(str(int(value, 16)))
            else:
                result.append(token_value)
            i += 1
        elif token_type == 'OPERATOR':
            if token_value == '&&':
                result.append('and')
            elif token_value == '||':
                result.append('or')
            elif token_value == '!':
                result.append('not ')
            elif token_value == 'CONCAT_START':
                i += 1
                if i < len(expr) and expr[i][0] == 'CONCAT':
                    concat_terms = expr[i][1]
                    translated_terms = []
                    for term in concat_terms:
                        if term[0] == 'IDENTIFIER':
                            translated_terms.append(f"self.{term[1]}.value")
                        else:
                            translated_terms.append(translate_expression([term]))
                    i += 1
                    i += 1
                    concat_expr = []
                    for idx, term in enumerate(reversed(translated_terms)):
                        concat_expr.append(f"({term} << {idx})")
                    result.append(" | ".join(concat_expr))
                else:
                    result.append("CONCAT_START")
            else:
                result.append(token_value)
            i += 1
        elif token_type == 'SYMBOL' and token_value == '{':
            concat_terms = []
            i += 1
            while i < len(expr) and expr[i][1] != '}':
                if expr[i][0] == 'IDENTIFIER':
                    concat_terms.append(f"self.{expr[i][1]}.value")
                elif expr[i][0] == 'SYMBOL' and expr[i][1] == ',':
                    i += 1
                    continue
                else:
                    concat_terms.append(translate_expression([expr[i]]))
                i += 1
            i += 1
            concat_expr = []
            for idx, term in enumerate(reversed(concat_terms)):
                concat_expr.append(f"({term} << {idx})")
            result.append(" | ".join(concat_expr))
        elif token_type == 'SYMBOL':
            result.append(token_value)
            i += 1
        elif token_type == 'STRING':
            result.append(f"'{token_value}'")
            i += 1
        elif token_type == 'KEYWORD' and token_value == '$time':
            result.append("self.time")
            i += 1
        else:
            i += 1
    
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
        false_statements = stmt.get('false_statements', [])
        code = [f"{indent_str}if {condition}:"]
        code.extend(true_code)
        if false_statements:
            if len(false_statements) == 1 and false_statements[0]['type'] == 'If':
                # Transforma o próximo If em elif
                next_if = false_statements[0]
                next_condition = translate_expression(next_if['condition'])
                next_true_code = [translate_statement(s, indent + 1) for s in next_if['true_statements']]
                next_false_statements = next_if.get('false_statements', [])
                code.append(f"{indent_str}elif {next_condition}:")
                code.extend(next_true_code)
                if next_false_statements:
                    code.append(f"{indent_str}else:")
                    code.extend([translate_statement(s, indent + 1) for s in next_false_statements])
            else:
                code.append(f"{indent_str}else:")
                code.extend([translate_statement(s, indent + 1) for s in false_statements])
        return "\n".join(code)
    return f"{indent_str}pass  # Declaração não suportada: {stmt['type']}"