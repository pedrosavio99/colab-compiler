from ..lexer.core import lexer
from ..parser.ast import ASTNode

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_iterator = iter(self.tokens)
        self.current_token = next(self.token_iterator, None)

    def parse(self):
        statements = []
        while self.current_token is not None:
            if self.current_token[0] == 'NEWLINE':
                self.current_token = next(self.token_iterator, None)
                continue
            if self.current_token[0] == 'DEDENT' and self.current_token[1] == '':
                self.current_token = next(self.token_iterator, None)
                break
            statement = self.parse_statement()
            statements.append(statement)
        return ASTNode('program', children=statements)

    def consume(self, token_type, token_value=None):
        if self.current_token is None:
            raise ValueError(f"Erro: Esperava '{token_type}' mas chegou ao fim dos tokens.")
        if self.current_token[0] != token_type:
            raise ValueError(f"Erro: Esperava '{token_type}' mas encontrou '{self.current_token[0]}'.")
        if token_value is not None and self.current_token[1] != token_value:
            raise ValueError(f"Erro: Esperava '{token_value}' mas encontrou '{self.current_token[1]}'.")
        token = self.current_token
        self.current_token = next(self.token_iterator, None)
        return ASTNode(token_type.lower(), value=token[1])

    def parse_statement(self):
        # Ignora NEWLINE antes de processar o statement
        while self.current_token and self.current_token[0] == 'NEWLINE':
            self.current_token = next(self.token_iterator, None)
        
        if self.current_token is None:
            return None
        
        token_type = self.current_token[0]
        if token_type == 'KEYWORD':
            if self.current_token[1] == 'if':
                return self.parse_if()
            elif self.current_token[1] == 'for':
                return self.parse_for()
            elif self.current_token[1] == 'while':
                return self.parse_while()
            elif self.current_token[1] == 'print':
                return self.parse_print()
            elif self.current_token[1] == 'else':
                return self.parse_else()  # Adicionar suporte para else, se necessário
        elif token_type == 'ID':
            return self.parse_assignment()
        # Adicione outros casos conforme necessário
        else:
            raise Exception(f"Erro: Token inesperado '{token_type}'.")

    def parse_if(self):
        self.consume('KEYWORD', 'if')
        condition = self.parse_expression()
        self.consume('COLON', ':')
        then_block = self.parse_block()
        else_block = None
        if self.current_token and self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'else':
            self.consume('KEYWORD', 'else')
            self.consume('COLON', ':')
            else_block = self.parse_block()
        return ASTNode('if', children=[condition, then_block, else_block] if else_block else [condition, then_block])

    def parse_for(self):
        self.consume('KEYWORD', 'for')
        loop_var = self.consume('ID')
        # Ignora tokens irrelevantes até 'in'
        while self.current_token and self.current_token[0] in ('NEWLINE', 'WHITESPACE'):
            self.current_token = next(self.token_iterator, None)
        if not (self.current_token and self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'in'):
            raise ValueError("Erro: Esperava 'in' após o identificador no 'for'.")
        self.consume('KEYWORD', 'in')
        limit = self.parse_expression()
        self.consume('COLON', ':')
        body = self.parse_block()
        return ASTNode('for', children=[loop_var, limit, body])

    def parse_while(self):
        self.consume('KEYWORD', 'while')
        condition = self.parse_expression()
        self.consume('COLON', ':')
        body = self.parse_block()
        return ASTNode('while', children=[condition, body])

    def parse_function(self):
        self.consume('KEYWORD', 'def')
        func_name = self.consume('ID').value
        self.consume('LPAREN', '(')
        params = []
        if self.current_token[0] != 'RPAREN':
            params.append(self.consume('ID'))
            while self.current_token[0] == 'COMMA':
                self.consume('COMMA', ',')
                params.append(self.consume('ID'))
        self.consume('RPAREN', ')')
        self.consume('COLON', ':')
        body = self.parse_block()
        return ASTNode('function', value=func_name, children=[ASTNode('parameters', children=params), body])

    def parse_print(self):
        self.consume('KEYWORD', 'print')
        self.consume('LPAREN', '(')
        expr = self.parse_expression()
        self.consume('RPAREN', ')')
        return ASTNode('print', children=[expr])

    def parse_assignment(self):
        identifier = self.consume('ID')
        self.consume('ASSIGN', '=')
        expr = self.parse_expression()
        return ASTNode('assignment', children=[identifier, expr])

    def parse_block(self):
        statements = []
        if self.current_token and self.current_token[0] == 'INDENT':
            self.consume('INDENT')
            while self.current_token and self.current_token[0] != 'DEDENT':
                # Ignora múltiplos NEWLINE antes de cada statement
                while self.current_token and self.current_token[0] == 'NEWLINE':
                    self.current_token = next(self.token_iterator, None)
                if self.current_token and self.current_token[0] != 'DEDENT':
                    statement = self.parse_statement()
                    if statement:
                        statements.append(statement)
                else:
                    break
            self.consume('DEDENT')
        else:
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        return ASTNode('block', children=statements)

    def parse_expression(self):
        return self.parse_logical()

    def parse_logical(self):
        expr = self.parse_comparison()
        while self.current_token and self.current_token[0] == 'KEYWORD' and self.current_token[1] in ('and', 'or'):
            op = self.current_token[1]
            self.current_token = next(self.token_iterator, None)
            right = self.parse_comparison()
            expr = ASTNode('logical', operator=op, children=[expr, right])
        return expr

    def parse_comparison(self):
        expr = self.parse_bitwise()
        while self.current_token and self.current_token[0] == 'OPERATOR' and self.current_token[1] in ('==', '!=', '<', '>', '<=', '>='):
            op = self.current_token[1]
            self.current_token = next(self.token_iterator, None)
            right = self.parse_bitwise()
            expr = ASTNode('comparison', operator=op, children=[expr, right])
        return expr

    def parse_bitwise(self):
        expr = self.parse_term()
        while self.current_token and self.current_token[0] == 'OPERATOR' and self.current_token[1] in ('&', '|', '^'):
            op = self.current_token[1]
            self.current_token = next(self.token_iterator, None)
            right = self.parse_term()
            expr = ASTNode('bitwise', operator=op, children=[expr, right])
        return expr

    def parse_term(self):
        expr = self.parse_factor()
        while self.current_token and self.current_token[0] == 'OPERATOR' and self.current_token[1] in ('+', '-'):
            op = self.current_token[1]
            self.current_token = next(self.token_iterator, None)
            right = self.parse_factor()
            expr = ASTNode('operation', operator=op, children=[expr, right])
        return expr

    def parse_factor(self):
        expr = self.parse_unary()
        while self.current_token and self.current_token[0] == 'OPERATOR' and self.current_token[1] in ('*', '/', '%'):
            op = self.current_token[1]
            self.current_token = next(self.token_iterator, None)
            right = self.parse_unary()
            expr = ASTNode('operation', operator=op, children=[expr, right])
        return expr

    def parse_unary(self):
        if self.current_token and self.current_token[0] == 'OPERATOR' and self.current_token[1] in ('-', 'not'):
            op = self.current_token[1]
            self.current_token = next(self.token_iterator, None)
            operand = self.parse_unary()
            return ASTNode('unary', operator=op, children=[operand])
        return self.parse_primary()

    def parse_primary(self):
        if self.current_token[0] == 'NUMBER':
            value = self.current_token[1]
            self.current_token = next(self.token_iterator, None)
            return ASTNode('number', value=float(value) if '.' in value else int(value))
        elif self.current_token[0] == 'STRING':
            value = self.current_token[1]
            self.current_token = next(self.token_iterator, None)
            return ASTNode('string', value=value)
        elif self.current_token[0] == 'KEYWORD' and self.current_token[1] in ('True', 'False'):
            value = self.current_token[1] == 'True'
            self.current_token = next(self.token_iterator, None)
            return ASTNode('bool', value=value)
        elif self.current_token[0] == 'ID':
            identifier = self.current_token[1]
            self.current_token = next(self.token_iterator, None)
            return ASTNode('identifier', value=identifier)
        elif self.current_token[0] == 'LPAREN':
            self.current_token = next(self.token_iterator, None)
            expr = self.parse_expression()
            self.consume('RPAREN', ')')
            return expr
        raise ValueError(f"Erro: Token inesperado '{self.current_token[0]}' na expressão.")