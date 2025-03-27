from .ast import ASTNode
from .expressions import parse_expression, parse_function_call

def parse_statement(tokens, token_index):
    if token_index[0] >= len(tokens):
        return None
    current_token = tokens[token_index[0]]

    if current_token[0] == 'ID':
        if token_index[0] + 1 < len(tokens) and tokens[token_index[0] + 1][0] == 'ASSIGN':
            return parse_assignment(tokens, token_index)
        else:
            return parse_function_call(tokens, token_index)
    elif current_token[0] == 'DEF':
        return parse_function_def(tokens, token_index)
    elif current_token[0] == 'RETURN':
        return parse_return_statement(tokens, token_index)
    elif current_token[0] in ('NEWLINE', 'INDENT', 'DEDENT'):
        return None
    else:
        raise SyntaxError(f"Token inesperado: {current_token}")

def parse_assignment(tokens, token_index):
    identifier = tokens[token_index[0]]
    token_index[0] += 1
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'ASSIGN':
        raise SyntaxError("Esperado '='")
    token_index[0] += 1
    expression = parse_expression(tokens, token_index)
    return ASTNode('assignment', children=[ASTNode('identifier', identifier[1]), expression])

def parse_function_def(tokens, token_index):
    token_index[0] += 1
    identifier = tokens[token_index[0]]
    token_index[0] += 1
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'LPAREN':
        raise SyntaxError("Esperado '('")
    token_index[0] += 1
    params = parse_param_list(tokens, token_index)
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'RPAREN':
        raise SyntaxError("Esperado ')'")
    token_index[0] += 1
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'COLON':
        raise SyntaxError("Esperado ':'")
    token_index[0] += 1
    if token_index[0] < len(tokens) and tokens[token_index[0]][0] == 'NEWLINE':
        token_index[0] += 1
    block = parse_block(tokens, token_index)
    return ASTNode('function_def', children=[ASTNode('identifier', identifier[1]), params, block])

def parse_return_statement(tokens, token_index):
    token_index[0] += 1
    expression = parse_expression(tokens, token_index)
    return ASTNode('return', children=[expression])

def parse_param_list(tokens, token_index):
    params = []
    while token_index[0] < len(tokens) and tokens[token_index[0]][0] != 'RPAREN':
        if tokens[token_index[0]][0] == 'ID':
            params.append(ASTNode('identifier', tokens[token_index[0]][1]))
            token_index[0] += 1
            if token_index[0] < len(tokens) and tokens[token_index[0]][0] == 'COMMA':
                token_index[0] += 1
        else:
            break
    return ASTNode('param_list', children=params)

def parse_block(tokens, token_index):
    statements = []
    if token_index[0] < len(tokens) and tokens[token_index[0]][0] == 'INDENT':
        token_index[0] += 1
        while token_index[0] < len(tokens) and tokens[token_index[0]][0] != 'DEDENT':
            stmt = parse_statement(tokens, token_index)
            if stmt:
                statements.append(stmt)
            if token_index[0] < len(tokens) and tokens[token_index[0]][0] == 'NEWLINE':
                token_index[0] += 1
        if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'DEDENT':
            raise SyntaxError("Esperado DEDENT")
        token_index[0] += 1
    return ASTNode('block', children=statements)