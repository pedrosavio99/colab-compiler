from .ast import ASTNode

def parse_expression(tokens, token_index):
    return parse_additive(tokens, token_index)

def parse_additive(tokens, token_index):
    left = parse_multiplicative(tokens, token_index)
    while token_index[0] < len(tokens) and tokens[token_index[0]][0] in ('PLUS', 'MINUS'):
        op = tokens[token_index[0]][1]
        token_index[0] += 1
        right = parse_multiplicative(tokens, token_index)
        left = ASTNode('binary_op', op, [left, right])
    return left

def parse_multiplicative(tokens, token_index):
    left = parse_factor(tokens, token_index)
    while token_index[0] < len(tokens) and tokens[token_index[0]][0] in ('MULT', 'DIV'):
        op = tokens[token_index[0]][1]
        token_index[0] += 1
        right = parse_factor(tokens, token_index)
        left = ASTNode('binary_op', op, [left, right])
    return left

def parse_factor(tokens, token_index):
    if token_index[0] >= len(tokens):
        raise SyntaxError("Fim inesperado dos tokens")
    current_token = tokens[token_index[0]]
    token_index[0] += 1
    if current_token[0] == 'NUMBER':
        return ASTNode('number', current_token[1])
    elif current_token[0] == 'ID':
        if token_index[0] < len(tokens) and tokens[token_index[0]][0] == 'LPAREN':
            token_index[0] -= 1
            return parse_function_call(tokens, token_index)
        return ASTNode('identifier', current_token[1])
    elif current_token[0] == 'STRING':
        return ASTNode('string', current_token[1])
    elif current_token[0] == 'LPAREN':
        expr = parse_expression(tokens, token_index)
        if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'RPAREN':
            raise SyntaxError("Esperado ')'")
        token_index[0] += 1
        return expr
    else:
        raise SyntaxError(f"Token inesperado: {current_token}")

def parse_function_call(tokens, token_index):
    func_name = tokens[token_index[0]][1]
    token_index[0] += 1
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'LPAREN':
        raise SyntaxError("Esperado '('")
    token_index[0] += 1
    args = parse_arg_list(tokens, token_index)
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'RPAREN':
        raise SyntaxError("Esperado ')'")
    token_index[0] += 1
    return ASTNode('function_call', func_name, children=args)

def parse_arg_list(tokens, token_index):
    args = []
    while token_index[0] < len(tokens) and tokens[token_index[0]][0] != 'RPAREN':
        args.append(parse_expression(tokens, token_index))
        if token_index[0] < len(tokens) and tokens[token_index[0]][0] == 'COMMA':
            token_index[0] += 1
    return args