from .ast import ASTNode

def parse_expression(tokens, token_index):
    return parse_logical(tokens, token_index)

def parse_logical(tokens, token_index):
    node = parse_comparison(tokens, token_index)
    while token_index[0] < len(tokens) and tokens[token_index[0]][0] == 'LOGICAL' and tokens[token_index[0]][1] in ('and', 'or'):
        operator = tokens[token_index[0]][1]
        token_index[0] += 1
        right = parse_comparison(tokens, token_index)
        node = ASTNode('logical', operator=operator, children=[node, right])
    return node

def parse_comparison(tokens, token_index):
    node = parse_bitwise(tokens, token_index)
    while token_index[0] < len(tokens) and tokens[token_index[0]][0] == 'COMPARISON':
        operator = tokens[token_index[0]][1]
        token_index[0] += 1
        right = parse_bitwise(tokens, token_index)
        node = ASTNode('comparison', operator=operator, children=[node, right])
    return node

def parse_bitwise(tokens, token_index):
    node = parse_add_sub(tokens, token_index)
    while token_index[0] < len(tokens) and tokens[token_index[0]][0] == 'BITWISE':
        operator = tokens[token_index[0]][1]
        token_index[0] += 1
        right = parse_add_sub(tokens, token_index)
        node = ASTNode('bitwise', operator=operator, children=[node, right])
    return node

def parse_add_sub(tokens, token_index):
    node = parse_mul_div(tokens, token_index)
    while token_index[0] < len(tokens) and tokens[token_index[0]][0] == 'OPERATOR' and tokens[token_index[0]][1] in ('+', '-'):
        operator = tokens[token_index[0]][1]
        token_index[0] += 1
        right = parse_mul_div(tokens, token_index)
        node = ASTNode('operation', operator=operator, children=[node, right])
    return node

def parse_mul_div(tokens, token_index):
    node = parse_unary(tokens, token_index)
    while token_index[0] < len(tokens) and tokens[token_index[0]][0] == 'OPERATOR' and tokens[token_index[0]][1] in ('*', '/', '%'):
        operator = tokens[token_index[0]][1]
        token_index[0] += 1
        right = parse_unary(tokens, token_index)
        node = ASTNode('operation', operator=operator, children=[node, right])
    return node

def parse_unary(tokens, token_index):
    if token_index[0] < len(tokens) and tokens[token_index[0]][0] in ('OPERATOR', 'BITWISE') and tokens[token_index[0]][1] in ('-', '~', 'not'):
        operator = tokens[token_index[0]][1]
        token_index[0] += 1
        operand = parse_factor(tokens, token_index)
        return ASTNode('unary', operator=operator, children=[operand])
    return parse_factor(tokens, token_index)

def parse_factor(tokens, token_index):
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] == 'NEWLINE':
        raise SyntaxError("Erro: O código terminou de forma inesperada. Esperava um valor.")
    current_token = tokens[token_index[0]]
    token_index[0] += 1

    if current_token[0] == 'LPAREN':
        expr = parse_expression(tokens, token_index)
        if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'RPAREN':
            raise SyntaxError("Erro: Parêntese não fechado.")
        token_index[0] += 1
        return expr
    elif current_token[0] == 'INVALID_NUMBER':
        if 'e' in current_token[1]:
            raise SyntaxError(f"Erro: 'e' não é permitido.")
        raise SyntaxError(f"Erro: '{current_token[1]}' não é um número válido.")
    elif current_token[0] == 'NUMBER':
        try:
            value = current_token[1]
            if '.' in value:
                parts = value.split('.')
                if len(parts) == 2 and parts[0].isdigit() and (parts[1].isdigit() or parts[1] == ''):
                    return ASTNode('number', float(value))
                raise ValueError
            if not value.isdigit():
                raise ValueError
            return ASTNode('number', int(value))
        except ValueError:
            raise SyntaxError(f"Erro: '{current_token[1]}' não é um número válido.")
    elif current_token[0] == 'KEYWORD' and current_token[1] in ('True', 'False'):
        return ASTNode('bool', current_token[1] == 'True')
    elif current_token[0] == 'ID':
        return ASTNode('identifier', current_token[1])
    elif current_token[0] == 'STRING':
        return ASTNode('string', current_token[1])
    elif current_token[0] == 'OPERATOR':
        raise SyntaxError(f"Erro: Operador '{current_token[1]}' não pode iniciar uma expressão.")
    elif current_token[0] == 'UNKNOWN':
        raise SyntaxError(f"Erro: '{current_token[1]}' não é permitido.")
    else:
        raise SyntaxError(f"Erro: '{current_token[1]}' não é permitido.")