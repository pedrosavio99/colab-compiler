import re

def lexer(code):
    token_specs = [
        ('IF', r'\bif\b'),
        ('ELSE', r'\belse\b'),
        ('WHILE', r'\bwhile\b'),
        ('FOR', r'\bfor\b'),
        ('DEF', r'\bdef\b'),
        ('RETURN', r'\breturn\b'),
        ('PLUS', r'\+'),
        ('MINUS', r'-'),
        ('MULT', r'\*'),
        ('DIV', r'/'),
        ('EQ', r'=='),
        ('NEQ', r'!='),
        ('LT', r'<'),
        ('GT', r'>'),
        ('LE', r'<='),
        ('GE', r'>='),
        ('ASSIGN', r'='),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('LBRACK', r'\['),
        ('RBRACK', r'\]'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('COMMA', r','),
        ('COLON', r':'),
        ('NUMBER', r'\b\d+\b'),
        ('ID', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
        ('STRING', r'"[^"]*"|\'[^\']*\''),
        ('WHITESPACE', r'[ \t]+'),
    ]
    
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specs)
    tokens = []
    lines = code.split('\n')
    indent_stack = [0]

    for line_num, line in enumerate(lines, 1):
        line = line.rstrip()
        if not line:
            continue

        indent_match = re.match(r'^(?:\s*)', line)
        indent_level = len(indent_match.group()) if indent_match else 0
        line = line[indent_level:]

        if indent_level > indent_stack[-1]:
            indent_stack.append(indent_level)
            tokens.append(('INDENT', ''))
        elif indent_level < indent_stack[-1]:
            while indent_level < indent_stack[-1]:
                indent_stack.pop()
                tokens.append(('DEDENT', ''))
            if indent_level != indent_stack[-1]:
                raise SyntaxError(f"Indentação inconsistente na linha {line_num}")

        pos = 0
        while pos < len(line):
            match = re.match(token_regex, line[pos:])
            if not match:
                raise SyntaxError(f"Caractere inválido na linha {line_num}: {line[pos:]}")
            kind = match.lastgroup
            value = match.group()
            if kind != 'WHITESPACE':
                tokens.append((kind, value))
            pos += match.end()

        tokens.append(('NEWLINE', '\n'))

    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(('DEDENT', ''))

    return tokens