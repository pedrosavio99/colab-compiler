from ..utils import logger

def handle_if(node, ast, module_stack, block_stack):
    if block_stack:
        block_stack[-1].children.append(node)
        block_stack.append(node)
        logger.debug("[Parser] Aninhado IF no bloco ativo e empilhado: %s", str(node))