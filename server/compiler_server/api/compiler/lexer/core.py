import re
from .tokens import TOKEN_REGEX
from .indentation import handle_indentation

def lexer(code):
    tokens = []
    lines = code.split('\n')
    indent_stack = [0]

    for line_num, line in enumerate(lines, 1):
        line = line.rstrip()
        if not line:
            continue

        line = handle_indentation(tokens, indent_stack, line, line_num)

        pos = 0
        while pos < len(line):
            match = re.match(TOKEN_REGEX, line[pos:])
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