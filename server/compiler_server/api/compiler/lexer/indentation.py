import re

def handle_indentation(tokens, indent_stack, line, line_num):
    indent_match = re.match(r'^(?:\s*)', line)
    indent_level = len(indent_match.group()) if indent_match else 0
    line_content = line[indent_level:]

    if indent_level > indent_stack[-1]:
        indent_stack.append(indent_level)
        tokens.append(('INDENT', '    '))
    elif indent_level < indent_stack[-1]:
        while indent_level < indent_stack[-1]:
            indent_stack.pop()
            tokens.append(('DEDENT', ''))
        if indent_level != indent_stack[-1]:
            raise SyntaxError(f"Erro na linha {line_num}: Nível de indentação inconsistente.")
    
    return line_content