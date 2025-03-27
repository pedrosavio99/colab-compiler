from .lexer import lexer

class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children else []

    def __str__(self):
        base = self.type
        if self.value:
            base += f"({self.value})"
        if self.children:
            children_str = ', '.join(str(child) for child in self.children)
            return f"{base}[{children_str}]"
        return base

token_index = 0

def parse(tokens):
    global token_index
    token_index = 0
    return parse_program(tokens)

def parse_program(tokens):
    global token_index
    statements = []
    while token_index < len(tokens) and tokens[token_index][0] != 'DEDENT':
        stmt = parse_statement(tokens)
        if stmt:
            statements.append(stmt)
        if token_index < len(tokens) and tokens[token_index][0] == 'NEWLINE':
            token_index += 1
    return ASTNode('program', children=statements)

def parse_statement(tokens):
    global token_index
    if token_index >= len(tokens):
        return None
    current_token = tokens[token_index]

    if current_token[0] == 'ID':
        if token_index + 1 < len(tokens) and tokens[token_index + 1][0] == 'ASSIGN':
            return parse_assignment(tokens)
        else:
            return parse_function_call(tokens)
    elif current_token[0] == 'DEF':
        return parse_function_def(tokens)
    elif current_token[0] == 'RETURN':
        return parse_return_statement(tokens)
    elif current_token[0] in ('NEWLINE', 'INDENT', 'DEDENT'):
        return None
    else:
        raise SyntaxError(f"Token inesperado: {current_token}")

def parse_assignment(tokens):
    global token_index
    identifier = tokens[token_index]
    token_index += 1
    if token_index >= len(tokens) or tokens[token_index][0] != 'ASSIGN':
        raise SyntaxError("Esperado '='")
    token_index += 1
    expression = parse_expression(tokens)
    return ASTNode('assignment', children=[ASTNode('identifier', identifier[1]), expression])

def parse_function_call(tokens):
    global token_index
    func_name = tokens[token_index][1]
    token_index += 1
    if token_index >= len(tokens) or tokens[token_index][0] != 'LPAREN':
        raise SyntaxError("Esperado '('")
    token_index += 1
    args = parse_arg_list(tokens)
    if token_index >= len(tokens) or tokens[token_index][0] != 'RPAREN':
        raise SyntaxError("Esperado ')'")
    token_index += 1
    return ASTNode('function_call', func_name, children=args)

def parse_arg_list(tokens):
    global token_index
    args = []
    while token_index < len(tokens) and tokens[token_index][0] != 'RPAREN':
        args.append(parse_expression(tokens))
        if token_index < len(tokens) and tokens[token_index][0] == 'COMMA':
            token_index += 1
    return args

def parse_function_def(tokens):
    global token_index
    token_index += 1
    identifier = tokens[token_index]
    token_index += 1
    if token_index >= len(tokens) or tokens[token_index][0] != 'LPAREN':
        raise SyntaxError("Esperado '('")
    token_index += 1
    params = parse_param_list(tokens)
    if token_index >= len(tokens) or tokens[token_index][0] != 'RPAREN':
        raise SyntaxError("Esperado ')'")
    token_index += 1
    if token_index >= len(tokens) or tokens[token_index][0] != 'COLON':
        raise SyntaxError("Esperado ':'")
    token_index += 1
    if token_index < len(tokens) and tokens[token_index][0] == 'NEWLINE':
        token_index += 1
    block = parse_block(tokens)
    return ASTNode('function_def', children=[ASTNode('identifier', identifier[1]), params, block])

def parse_return_statement(tokens):
    global token_index
    token_index += 1
    expression = parse_expression(tokens)
    return ASTNode('return', children=[expression])

def parse_param_list(tokens):
    global token_index
    params = []
    while token_index < len(tokens) and tokens[token_index][0] != 'RPAREN':
        if tokens[token_index][0] == 'ID':
            params.append(ASTNode('identifier', tokens[token_index][1]))
            token_index += 1
            if token_index < len(tokens) and tokens[token_index][0] == 'COMMA':
                token_index += 1
        else:
            break
    return ASTNode('param_list', children=params)

def parse_block(tokens):
    global token_index
    statements = []
    if token_index < len(tokens) and tokens[token_index][0] == 'INDENT':
        token_index += 1
        while token_index < len(tokens) and tokens[token_index][0] != 'DEDENT':
            stmt = parse_statement(tokens)
            if stmt:
                statements.append(stmt)
            if token_index < len(tokens) and tokens[token_index][0] == 'NEWLINE':
                token_index += 1
        if token_index >= len(tokens) or tokens[token_index][0] != 'DEDENT':
            raise SyntaxError("Esperado DEDENT")
        token_index += 1
    return ASTNode('block', children=statements)

def parse_expression(tokens):
    return parse_additive(tokens)

def parse_additive(tokens):
    global token_index
    left = parse_multiplicative(tokens)
    while token_index < len(tokens) and tokens[token_index][0] in ('PLUS', 'MINUS'):
        op = tokens[token_index][1]
        token_index += 1
        right = parse_multiplicative(tokens)
        left = ASTNode('binary_op', op, [left, right])
    return left

def parse_multiplicative(tokens):
    global token_index
    left = parse_factor(tokens)
    while token_index < len(tokens) and tokens[token_index][0] in ('MULT', 'DIV'):
        op = tokens[token_index][1]
        token_index += 1
        right = parse_factor(tokens)
        left = ASTNode('binary_op', op, [left, right])
    return left

def parse_factor(tokens):
    global token_index
    if token_index >= len(tokens):
        raise SyntaxError("Fim inesperado dos tokens")
    current_token = tokens[token_index]
    token_index += 1
    if current_token[0] == 'NUMBER':
        return ASTNode('number', current_token[1])
    elif current_token[0] == 'ID':
        if token_index < len(tokens) and tokens[token_index][0] == 'LPAREN':
            token_index -= 1
            return parse_function_call(tokens)
        return ASTNode('identifier', current_token[1])
    elif current_token[0] == 'STRING':
        return ASTNode('string', current_token[1])
    elif current_token[0] == 'LPAREN':
        expr = parse_expression(tokens)
        if token_index >= len(tokens) or tokens[token_index][0] != 'RPAREN':
            raise SyntaxError("Esperado ')'")
        token_index += 1
        return expr
    else:
        raise SyntaxError(f"Token inesperado: {current_token}")