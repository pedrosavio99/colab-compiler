from ..utils import logger

def handle_assign_print(node, ast, module_stack, block_stack):
    if block_stack:
        block_stack[-1].children.append(node)
        logger.debug("[Parser] Aninhado %s no bloco ativo: %s", node.type, str(node))
    elif module_stack:
        module_stack[-1].children.append(node)
        logger.debug("[Parser] Aninhado %s no MODULE: %s", node.type, str(node))
    else:
        ast.append(node)
        logger.debug("[Parser] Adicionado %s à AST (fora de módulo): %s", node.type, str(node))