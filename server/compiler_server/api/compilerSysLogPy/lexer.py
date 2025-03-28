def lexer(code):
    tokens = []
    keywords = {
        'module', 'endmodule', 'input', 'output', 'inout', 'wire', 'reg',
        'always', 'begin', 'end', 'if', 'else', 'assign', 'posedge', 'negedge', 'or',
        '$monitor', '$time', '$finish', 'initial'  # Adicionado 'initial'
    }
    operators = {
        '+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '&&', '||',
        '!', '&', '|', '^', '~', '<<', '>>', '=', ':', '#' 
    }
    
    print("Iniciando lexer...")
    i = 0
    while i < len(code):
        char = code[i]

        if char.isspace():
            i += 1
            continue

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

        if char == '"':  # Tratamento de strings
            i += 1
            string = ''
            while i < len(code) and code[i] != '"':
                string += code[i]
                i += 1
            i += 1  # Pula o '"'
            token = ('STRING', string)
            tokens.append(token)
            print(f"Token adicionado: {token}")
            continue

        if char.isalpha() or char == '_' or char == '$':
            word = ''
            while i < len(code) and (code[i].isalnum() or code[i] in '_$'):
                word += code[i]
                i += 1
            token = ('KEYWORD', word) if word in keywords else ('IDENTIFIER', word)
            tokens.append(token)
            print(f"Token adicionado: {token}")
            continue

        if char.isdigit() or (char == "'" and i > 0 and code[i - 1].isdigit()):
            num = char
            i += 1
            while i < len(code) and (code[i].isdigit() or code[i] in "'bhdx"):
                num += code[i]
                i += 1
            token = ('NUMBER', num)
            tokens.append(token)
            print(f"Token adicionado: {token}")
            continue

        op = char
        if i + 1 < len(code) and char + code[i + 1] in operators:
            op = char + code[i + 1]
            i += 2
        elif char in operators:
            i += 1
        if op in operators:
            token = ('OPERATOR', op)
            tokens.append(token)
            print(f"Token adicionado: {token}")
            continue

        if char in '();,[]{}@':
            token = ('SYMBOL', char)
            tokens.append(token)
            print(f"Token adicionado: {token}")
            i += 1
            continue

        token = ('UNKNOWN', char)
        tokens.append(token)
        print(f"Token desconhecido: {token}")
        i += 1

    print("Lexer concluído. Tokens gerados:", tokens)
    return tokens