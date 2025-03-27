from .statements import parse_statement
from .ast import ASTNode

def parse(tokens):
    token_index = [0]  # Usamos uma lista pra permitir mutação nas funções
    ast = parse_program(tokens, token_index)
    return ast

def parse_program(tokens, token_index):
    statements = []
    while token_index[0] < len(tokens) and tokens[token_index[0]][0] != 'DEDENT':
        stmt = parse_statement(tokens, token_index)
        if stmt:
            statements.append(stmt)
        if token_index[0] < len(tokens) and tokens[token_index[0]][0] == 'NEWLINE':
            token_index[0] += 1
    return ASTNode('program', children=statements)