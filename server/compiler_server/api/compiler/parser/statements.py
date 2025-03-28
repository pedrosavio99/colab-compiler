from .ast import ASTNode
from .expressions import parse_expression

def parse_statement(tokens, token_index):
    if token_index[0] >= len(tokens):
        return None
    current_token = tokens[token_index[0]]
    if current_token[0] == 'KEYWORD':
        if current_token[1] == 'if':
            return parse_if(tokens, token_index)
        elif current_token[1] == 'for':
            return parse_for(tokens, token_index)
        elif current_token[1] == 'while':
            return parse_while(tokens, token_index)
        elif current_token[1] == 'def':
            return parse_function(tokens, token_index)
        elif current_token[1] == 'print':
            return parse_print(tokens, token_index)  # Adicionado suporte para print
        else:
            raise SyntaxError(f"Erro: '{current_token[1]}' não é permitido.")
    elif current_token[0] == 'ID':
        if token_index[0] + 1 < len(tokens) and tokens[token_index[0] + 1][0] == 'ASSIGN':
            return parse_assignment(tokens, token_index)
        else:
            raise SyntaxError(f"Erro: Esperava '=' após '{current_token[1]}'.")
    elif current_token[0] == 'NEWLINE':
        token_index[0] += 1
        return None
    elif current_token[0] == 'UNKNOWN':
        raise SyntaxError(f"Erro: '{current_token[1]}' não é permitido.")
    else:
        raise SyntaxError(f"Erro: '{current_token[1]}' não é permitido.")

def parse_print(tokens, token_index):
    token_index[0] += 1  # Consome 'print'
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'LPAREN':
        raise SyntaxError("Erro: Esperava '(' após 'print'.")
    token_index[0] += 1
    expr = parse_expression(tokens, token_index)
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'RPAREN':
        raise SyntaxError("Erro: Esperava ')' após o argumento de 'print'.")
    token_index[0] += 1
    return ASTNode('print', children=[expr])

def parse_assignment(tokens, token_index):
    identifier = tokens[token_index[0]]
    token_index[0] += 1
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'ASSIGN':
        raise SyntaxError(f"Erro: Esperava '=' após '{identifier[1]}'.")
    token_index[0] += 1
    expression = parse_expression(tokens, token_index)
    return ASTNode('assignment', children=[ASTNode('identifier', identifier[1]), expression])

def parse_if(tokens, token_index):
    token_index[0] += 1  # Consome 'if'
    condition = parse_expression(tokens, token_index)
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'NEWLINE':
        raise SyntaxError("Erro: Esperava nova linha após a condição do 'if'.")
    token_index[0] += 1
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'INDENT':
        raise SyntaxError("Erro: Esperava indentação após 'if'.")
    token_index[0] += 1
    then_block = parse_block(tokens, token_index)
    else_block = None
    if token_index[0] < len(tokens) and tokens[token_index[0]][0] == 'KEYWORD' and tokens[token_index[0]][1] == 'else':
        token_index[0] += 1
        if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'NEWLINE':
            raise SyntaxError("Erro: Esperava nova linha após 'else'.")
        token_index[0] += 1
        if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'INDENT':
            raise SyntaxError("Erro: Esperava indentação após 'else'.")
        token_index[0] += 1
        else_block = parse_block(tokens, token_index)
    return ASTNode('if', children=[condition, then_block, else_block] if else_block else [condition, then_block])

def parse_for(tokens, token_index):
    token_index[0] += 1  # Consome 'for'
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'ID':
        raise SyntaxError("Erro: Esperava um identificador após 'for'.")
    loop_var = tokens[token_index[0]][1]
    token_index[0] += 1
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'KEYWORD' or tokens[token_index[0]][1] != 'in':
        raise SyntaxError("Erro: Esperava 'in' após o identificador no 'for'.")
    token_index[0] += 1
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'ID' or tokens[token_index[0]][1] != 'range':
        raise SyntaxError("Erro: Esperava 'range' no 'for'.")
    token_index[0] += 1
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'LPAREN':
        raise SyntaxError("Erro: Esperava '(' após 'range'.")
    token_index[0] += 1
    limit = parse_expression(tokens, token_index)
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'RPAREN':
        raise SyntaxError("Erro: Esperava ')' após o argumento de 'range'.")
    token_index[0] += 1
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'NEWLINE':
        raise SyntaxError("Erro: Esperava nova linha após 'for'.")
    token_index[0] += 1
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'INDENT':
        raise SyntaxError("Erro: Esperava indentação após 'for'.")
    token_index[0] += 1
    body = parse_block(tokens, token_index)
    return ASTNode('for', children=[ASTNode('identifier', loop_var), limit, body])

def parse_while(tokens, token_index):
    token_index[0] += 1  # Consome 'while'
    condition = parse_expression(tokens, token_index)
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'NEWLINE':
        raise SyntaxError("Erro: Esperava nova linha após a condição do 'while'.")
    token_index[0] += 1
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'INDENT':
        raise SyntaxError("Erro: Esperava indentação após 'while'.")
    token_index[0] += 1
    body = parse_block(tokens, token_index)
    return ASTNode('while', children=[condition, body])

def parse_function(tokens, token_index):
    token_index[0] += 1  # Consome 'def'
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'ID':
        raise SyntaxError("Erro: Esperava um nome de função após 'def'.")
    func_name = tokens[token_index[0]][1]
    token_index[0] += 1
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'LPAREN':
        raise SyntaxError("Erro: Esperava '(' após o nome da função.")
    token_index[0] += 1
    params = []
    while token_index[0] < len(tokens) and tokens[token_index[0]][0] != 'RPAREN':
        if tokens[token_index[0]][0] != 'ID':
            raise SyntaxError("Erro: Esperava um identificador como parâmetro.")
        params.append(ASTNode('identifier', tokens[token_index[0]][1]))
        token_index[0] += 1
        if token_index[0] < len(tokens) and tokens[token_index[0]][0] == 'COMMA':
            token_index[0] += 1
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'RPAREN':
        raise SyntaxError("Erro: Esperava ')' após os parâmetros da função.")
    token_index[0] += 1
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'NEWLINE':
        raise SyntaxError("Erro: Esperava nova linha após 'def'.")
    token_index[0] += 1
    if token_index[0] >= len(tokens) or tokens[token_index[0]][0] != 'INDENT':
        raise SyntaxError("Erro: Esperava indentação após 'def'.")
    token_index[0] += 1
    body = parse_block(tokens, token_index)
    return ASTNode('function', value=func_name, children=[ASTNode('parameters', children=params), body])

def parse_block(tokens, token_index):
    statements = []
    while token_index[0] < len(tokens) and tokens[token_index[0]][0] != 'DEDENT':
        stmt = parse_statement(tokens, token_index)
        if stmt:
            statements.append(stmt)
    if token_index[0] < len(tokens) and tokens[token_index[0]][0] == 'DEDENT':
        token_index[0] += 1
    return ASTNode('block', children=statements)