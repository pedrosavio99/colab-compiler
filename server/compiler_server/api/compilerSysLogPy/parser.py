class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        print("Iniciando parser com tokens:", tokens)

    def current_token(self):
        token = self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)
        print(f"Token atual (pos {self.pos}): {token}")
        return token

    def consume(self, expected_type=None, expected_value=None):
        token_type, token_value = self.current_token()
        if (expected_type and token_type != expected_type) or (expected_value and token_value != expected_value):
            raise ValueError(f"Esperado {expected_type} {expected_value}, encontrado {token_type} {token_value}")
        self.pos += 1
        print(f"Consumido: ({token_type}, {token_value})")
        return token_type, token_value

    def parse(self):
        ast = {'type': 'Program', 'body': []}
        print("Parsing programa...")
        while self.pos < len(self.tokens):
            token_type, token_value = self.current_token()
            if token_type == 'KEYWORD' and token_value == 'module':
                ast['body'].append(self.parse_module())
            else:
                self.pos += 1
        print("AST gerado:", ast)
        return ast

    def parse_module(self):
        print("Parsing module...")
        self.consume('KEYWORD', 'module')
        _, module_name = self.consume('IDENTIFIER')
        
        ports = []
        if self.current_token()[1] == '(':  # Portas são opcionais
            self.consume('SYMBOL', '(')
            while self.current_token()[1] != ')':
                ports.append(self.parse_port())
                if self.current_token()[1] == ',':
                    self.consume('SYMBOL', ',')
            self.consume('SYMBOL', ')')
        
        self.consume('SYMBOL', ';')  # Sempre espera ';' após o cabeçalho do módulo

        body = []
        while self.pos < len(self.tokens) and self.current_token()[1] != 'endmodule':
            token_type, token_value = self.current_token()
            if token_value in ('input', 'output', 'inout', 'wire', 'reg'):
                body.append(self.parse_declaration())
            elif token_value == 'assign':
                body.append(self.parse_assign())
            elif token_value == 'always':
                body.append(self.parse_always())
            elif token_value == 'initial':
                body.append(self.parse_initial())
            else:
                print(f"Ignorando token no corpo do módulo: {token_type} {token_value}")
                self.pos += 1
        self.consume('KEYWORD', 'endmodule')
        return {'type': 'Module', 'name': module_name, 'ports': ports, 'body': body}

    def parse_bit_width(self):
        if self.current_token()[1] != '[':
            return None
        self.consume('SYMBOL', '[')
        
        high = 0
        if self.current_token()[0] == 'NUMBER':
            _, high = self.consume('NUMBER')
        
        self.consume('OPERATOR', ':')
        
        low = 0
        if self.current_token()[0] == 'NUMBER':
            _, low = self.consume('NUMBER')
        
        self.consume('SYMBOL', ']')
        return (int(high), int(low))

    def parse_port(self):
        print("Parsing port...")
        port_type = self.current_token()[1]
        if port_type in ('input', 'output', 'inout'):
            self.consume('KEYWORD')
        
        data_type = None
        if self.current_token()[1] in ('reg', 'wire'):
            data_type = self.current_token()[1]
            self.consume('KEYWORD')

        bit_width = None
        if self.current_token()[1] == '[':
            bit_width = self.parse_bit_width()

        _, port_name = self.consume('IDENTIFIER')
        return {'type': port_type, 'name': port_name, 'data_type': data_type, 'bit_width': bit_width}

    def parse_declaration(self):
        print("Parsing declaration...")
        decl_type = self.current_token()[1]
        self.consume('KEYWORD')

        bit_width = None
        if self.current_token()[1] == '[':
            bit_width = self.parse_bit_width()

        _, name = self.consume('IDENTIFIER')
        
        initial_value = None
        if self.current_token()[1] == '=':
            self.consume('OPERATOR', '=')
            _, initial_value = self.consume('NUMBER')
            initial_value = int(initial_value)
        
        self.consume('SYMBOL', ';')
        return {
            'type': 'Declaration', 
            'decl_type': decl_type, 
            'name': name, 
            'bit_width': bit_width, 
            'initial_value': initial_value
        }

    def parse_assign(self):
        print("Parsing assign...")
        self.consume('KEYWORD', 'assign')
        _, lhs = self.consume('IDENTIFIER')
        self.consume('OPERATOR', '=')
        rhs = self.parse_expression()
        self.consume('SYMBOL', ';')
        return {'type': 'Assign', 'lhs': lhs, 'rhs': rhs}

    def parse_always(self):
        print("Parsing always...")
        self.consume('KEYWORD', 'always')
        
        delay = None
        sensitivity_list = []
        token_type, token_value = self.current_token()
        
        if token_value == '#':
            self.consume('OPERATOR', '#')
            _, delay_value = self.consume('NUMBER')
            delay = int(delay_value)
            
            _, lhs = self.consume('IDENTIFIER')
            self.consume('OPERATOR', '=')
            rhs = self.parse_expression()
            self.consume('SYMBOL', ';')
            
            return {'type': 'AlwaysDelay', 'delay': delay, 'statement': {'type': 'Assignment', 'lhs': lhs, 'rhs': rhs}}
        
        elif token_value == '@':
            self.consume('SYMBOL', '@')
            
            has_paren = self.current_token()[1] == '('
            if has_paren:
                self.consume('SYMBOL', '(')
            
            while True:
                edge = None
                if self.current_token()[1] in ('posedge', 'negedge'):
                    edge = self.current_token()[1]
                    self.consume('KEYWORD')
                
                _, signal = self.consume('IDENTIFIER')
                sensitivity_list.append({'edge': edge, 'signal': signal})
                
                next_token = self.current_token()
                if has_paren and next_token[1] == ')':
                    break
                elif not has_paren and next_token[1] == 'begin':
                    break
                elif next_token[1] in (',', 'or'):
                    self.consume()
                else:
                    raise ValueError(f"Esperado ',', 'or' ou ')', encontrado {next_token[1]}")
            
            if has_paren:
                self.consume('SYMBOL', ')')
            
            self.consume('KEYWORD', 'begin')
            
            statements = []
            while self.current_token()[1] != 'end':
                statements.append(self.parse_statement())
            
            self.consume('KEYWORD', 'end')
            return {'type': 'Always', 'sensitivity_list': sensitivity_list, 'statements': statements}
        
        else:
            raise ValueError(f"Esperado '@' ou '#', encontrado {token_value}")

    def parse_initial(self):
        print("Parsing initial...")
        self.consume('KEYWORD', 'initial')
        self.consume('KEYWORD', 'begin')
        
        statements = []
        while self.current_token()[1] != 'end':
            token_type, token_value = self.current_token()
            if token_value == '$monitor':
                statements.append(self.parse_monitor())
            elif token_value == '#':
                statements.append(self.parse_delay())
            else:
                statements.append(self.parse_statement())
        
        self.consume('KEYWORD', 'end')
        return {'type': 'Initial', 'statements': statements}

    def parse_monitor(self):
        print("Parsing $monitor...")
        self.consume('KEYWORD', '$monitor')
        self.consume('SYMBOL', '(')
        
        args = []
        while self.current_token()[1] != ')':
            if self.current_token()[0] == 'STRING':
                _, string = self.consume('STRING')
                args.append({'type': 'String', 'value': string})
            else:
                args.append({'type': 'Expression', 'value': self.parse_expression()})
            if self.current_token()[1] == ',':
                self.consume('SYMBOL', ',')
        
        self.consume('SYMBOL', ')')
        self.consume('SYMBOL', ';')
        return {'type': 'Monitor', 'args': args}

    def parse_delay(self):
        print("Parsing delay...")
        self.consume('OPERATOR', '#')
        _, delay_value = self.consume('NUMBER')
        
        if self.current_token()[1] == '$finish':
            self.consume('KEYWORD', '$finish')
            self.consume('SYMBOL', ';')
            return {'type': 'Finish', 'delay': int(delay_value)}
        else:
            _, lhs = self.consume('IDENTIFIER')
            self.consume('OPERATOR', '=')  # Suporta '='
            rhs = self.parse_expression()
            self.consume('SYMBOL', ';')
            return {'type': 'DelayAssignment', 'delay': int(delay_value), 'lhs': lhs, 'rhs': rhs}

    def parse_statement(self):
        print("Parsing statement...")
        token_type, token_value = self.current_token()
        if token_value == 'if':
            return self.parse_if()
        else:
            _, lhs = self.consume('IDENTIFIER')
            op_type, op_value = self.consume('OPERATOR')  # Suporta '=' ou '<='
            if op_value not in ('=', '<='):
                raise ValueError(f"Esperado '=' ou '<=', encontrado {op_value}")
            rhs = self.parse_expression()
            self.consume('SYMBOL', ';')
            return {'type': 'Assignment', 'lhs': lhs, 'rhs': rhs, 'operator': op_value}

    def parse_if(self):
        print("Parsing if...")
        self.consume('KEYWORD', 'if')
        self.consume('SYMBOL', '(')
        condition = self.parse_expression()
        self.consume('SYMBOL', ')')
        
        true_statements = []
        if self.current_token()[1] == 'begin':
            self.consume('KEYWORD', 'begin')
            while self.current_token()[1] != 'end':
                true_statements.append(self.parse_statement())
            self.consume('KEYWORD', 'end')
        else:
            true_statements.append(self.parse_statement())
        
        false_statements = []
        if self.current_token()[1] == 'else':
            self.consume('KEYWORD', 'else')
            if self.current_token()[1] == 'begin':
                self.consume('KEYWORD', 'begin')
                while self.current_token()[1] != 'end':
                    false_statements.append(self.parse_statement())
                self.consume('KEYWORD', 'end')
            else:
                false_statements.append(self.parse_statement())
        
        return {'type': 'If', 'condition': condition, 'true_statements': true_statements, 'false_statements': false_statements}

    def parse_expression(self):
        print("Parsing expression...")
        expr = []
        while self.current_token()[1] not in (';', ')', ',', 'begin', 'end'):
            token_type, token_value = self.current_token()
            if token_type in ('IDENTIFIER', 'NUMBER', 'STRING'):
                expr.append((token_type, token_value))
            elif token_type == 'OPERATOR':
                expr.append((token_type, token_value))
            elif token_value == '(':
                expr.append(('SYMBOL', '('))
                self.consume()
                expr.extend(self.parse_expression())
                self.consume('SYMBOL', ')')
                expr.append(('SYMBOL', ')'))
                continue
            self.consume()
        print(f"Expressão parseada: {expr}")
        return expr

def parse(tokens):
    parser = Parser(tokens)
    return parser.parse()