# api/compilerSysLogPy/lexer.py

def lexer(code):
    tokens = []
    keywords = {
        'module', 'endmodule', 'input', 'output', 'inout', 'wire', 'reg',
        'always', 'begin', 'end', 'if', 'else', 'assign', 'posedge', 'negedge', 'or'
    }
    operators = {
        '+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '&&', '||',
        '!', '&', '|', '^', '~', '<<', '>>', '=', ':'
    }
    
    i = 0
    while i < len(code):
        char = code[i]

        # Ignorar espaços e quebras de linha
        if char.isspace():
            i += 1
            continue

        # Comentários
        if char == '/' and i + 1 < len(code):
            if code[i + 1] == '/':
                while i < len(code) and code[i] != '\n':
                    i += 1
                continue
            elif code[i + 1] == '*':
                i += 2
                while i < len(code) and not (code[i - 1] == '*' and code[i] == '/'):
                    i += 1
                i += 1
                continue

        # Identificadores e palavras-chave
        if char.isalpha() or char == '_':
            word = ''
            while i < len(code) and (code[i].isalnum() or code[i] == '_'):
                word += code[i]
                i += 1
            tokens.append(('KEYWORD', word) if word in keywords else ('IDENTIFIER', word))
            continue

        # Números
        if char.isdigit() or (char == "'" and i > 0 and code[i - 1].isdigit()):
            num = char
            i += 1
            while i < len(code) and (code[i].isdigit() or code[i] in "'bhdx"):
                num += code[i]
                i += 1
            tokens.append(('NUMBER', num))
            continue

        # Operadores
        op = char
        if i + 1 < len(code) and char + code[i + 1] in operators:
            op = char + code[i + 1]
            i += 2
        elif char in operators:
            i += 1
        if op in operators:
            tokens.append(('OPERATOR', op))
            continue

        # Símbolos (incluindo @)
        if char in '();,[]{}@':
            tokens.append(('SYMBOL', char))
            i += 1
            continue

        # Desconhecido
        tokens.append(('UNKNOWN', char))
        i += 1

    return tokens