from ..utils import logger

def handle_initial_start(node, ast, module_stack, block_stack):
    if block_stack:
        block_stack[-1].children.append(node)
        logger.debug("[Parser] Aninhado INITIAL_START no bloco ativo: %s", str(node))
    elif module_stack:
        module_stack[-1].children.append(node)
        logger.debug("[Parser] Aninhado INITIAL_START no MODULE: %s", str(node))
    else:
        ast.append(node)
        logger.debug("[Parser] Adicionado INITIAL_START à AST (fora de módulo): %s", str(node))