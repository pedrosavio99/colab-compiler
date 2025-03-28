# api/compilerSysLogPy/parser.py

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def consume(self, expected_type=None, expected_value=None):
        token_type, token_value = self.current_token()
        if (expected_type and token_type != expected_type) or (expected_value and token_value != expected_value):
            raise ValueError(f"Esperado {expected_type} {expected_value}, encontrado {token_type} {token_value}")
        self.pos += 1
        return token_type, token_value

    def parse(self):
        ast = {'type': 'Program', 'body': []}
        while self.pos < len(self.tokens):
            token_type, token_value = self.current_token()
            if token_type == 'KEYWORD' and token_value == 'module':
                ast['body'].append(self.parse_module())
            else:
                self.pos += 1
        return ast

    def parse_module(self):
        self.consume('KEYWORD', 'module')
        _, module_name = self.consume('IDENTIFIER')
        self.consume('SYMBOL', '(')
        
        ports = []
        while self.current_token()[1] != ')':
            ports.append(self.parse_port())
            if self.current_token()[1] == ',':
                self.consume('SYMBOL', ',')
        self.consume('SYMBOL', ')')
        
        # Ponto e vírgula opcional
        if self.current_token()[1] == ';':
            self.consume('SYMBOL', ';')

        body = []
        while self.pos < len(self.tokens) and self.current_token()[1] != 'endmodule':
            token_type, token_value = self.current_token()
            if token_value in ('input', 'output', 'inout', 'wire', 'reg'):
                body.append(self.parse_declaration())
            elif token_value == 'assign':
                body.append(self.parse_assign())
            elif token_value == 'always':
                body.append(self.parse_always())
            else:
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
        decl_type = self.current_token()[1]
        self.consume('KEYWORD')

        bit_width = None
        if self.current_token()[1] == '[':
            bit_width = self.parse_bit_width()

        _, name = self.consume('IDENTIFIER')
        self.consume('SYMBOL', ';')
        return {'type': 'Declaration', 'decl_type': decl_type, 'name': name, 'bit_width': bit_width}

    def parse_assign(self):
        self.consume('KEYWORD', 'assign')
        _, lhs = self.consume('IDENTIFIER')
        self.consume('OPERATOR', '=')
        rhs = self.parse_expression()
        self.consume('SYMBOL', ';')
        return {'type': 'Assign', 'lhs': lhs, 'rhs': rhs}

    def parse_always(self):
        self.consume('KEYWORD', 'always')
        self.consume('SYMBOL', '@')
        
        has_paren = self.current_token()[1] == '('
        if has_paren:
            self.consume('SYMBOL', '(')
        
        sensitivity_list = []
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


    def parse_statement(self):
        token_type, token_value = self.current_token()
        if token_value == 'if':
            return self.parse_if()
        else:
            _, lhs = self.consume('IDENTIFIER')
            self.consume('OPERATOR', '=')
            rhs = self.parse_expression()
            self.consume('SYMBOL', ';')
            return {'type': 'Assignment', 'lhs': lhs, 'rhs': rhs}

    def parse_if(self):
        self.consume('KEYWORD', 'if')           # Consome a palavra-chave 'if'
        self.consume('SYMBOL', '(')             # Consome o parêntese de abertura
        condition = self.parse_expression()     # Analisa a condição dentro dos parênteses
        self.consume('SYMBOL', ')')             # Consome o parêntese de fechamento
        
        true_statements = []                    # Lista para as instruções do ramo verdadeiro
        if self.current_token()[1] == 'begin':  # Verifica se há um bloco 'begin'
            self.consume('KEYWORD', 'begin')
            while self.current_token()[1] != 'end':  # Analisa todas as instruções até 'end'
                true_statements.append(self.parse_statement())
            self.consume('KEYWORD', 'end')
        else:                                   # Caso de instrução única
            true_statements.append(self.parse_statement())
        
        false_statements = []                   # Lista para as instruções do ramo falso
        if self.current_token()[1] == 'else':   # Verifica se há um 'else'
            self.consume('KEYWORD', 'else')
            if self.current_token()[1] == 'begin':  # Verifica se há um bloco 'begin' no 'else'
                self.consume('KEYWORD', 'begin')
                while self.current_token()[1] != 'end':  # Analisa até 'end'
                    false_statements.append(self.parse_statement())
                self.consume('KEYWORD', 'end')
            else:                               # Caso de instrução única no 'else'
                false_statements.append(self.parse_statement())
        
        return {'type': 'If', 'condition': condition, 'true_statements': true_statements, 'false_statements': false_statements}

    def parse_expression(self):
        expr = []
        while self.current_token()[1] not in (';', ')', ',', 'begin', 'end'):
            token_type, token_value = self.current_token()
            if token_type in ('IDENTIFIER', 'NUMBER'):
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
        return expr


def parse(tokens):
    parser = Parser(tokens)
    return parser.parse()