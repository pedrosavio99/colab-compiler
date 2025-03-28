def sanitize_name(name):
    return ''.join(c if c.isalnum() else '_' for c in name)

def find_identifiers(node):
    identifiers = set()
    if node.type == 'identifier':
        identifiers.add(node.value)
    elif node.type in ('operation', 'logical', 'bitwise', 'comparison', 'unary'):
        for child in node.children:
            identifiers.update(find_identifiers(child))
    return identifiers

def check_for_string_op(node):
    if node.type == 'block':
        for child in node.children:
            if check_for_string_op(child):
                return True
    elif node.type == 'function':
        return check_for_string_op(node.children[1])  # Verifica o corpo da função
    elif node.type in ('operation', 'logical', 'bitwise', 'comparison'):
        return any(check_for_string_op(child) for child in node.children)
    elif node.type == 'unary':
        return check_for_string_op(node.children[0])
    elif node.type == 'string':
        return True
    return False