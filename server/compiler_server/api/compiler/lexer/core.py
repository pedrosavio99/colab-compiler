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
            if match:
                kind = match.lastgroup
                value = match.group()
                if kind == 'STRING':
                    if not (value.startswith('"') and value.endswith('"')) and not (value.startswith("'") and value.endswith("'")):
                        tokens.append(('UNKNOWN', value[0]))
                        pos += 1
                        while pos < len(line) and line[pos] not in ' \t\n':
                            tokens.append(('UNKNOWN', line[pos]))
                            pos += 1
                        continue
                    tokens.append(('STRING', value))
                elif kind != 'WHITESPACE':
                    tokens.append((kind, value))
                pos += match.end()
            else:
                tokens.append(('UNKNOWN', line[pos]))
                pos += 1
        print(f"Linha {line_num}: {line} -> Tokens: {tokens[-5:]}")
        tokens.append(('NEWLINE', '\n'))

    # Fechar todos os níveis de indentação no final do arquivo
    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(('DEDENT', ''))

    return tokens