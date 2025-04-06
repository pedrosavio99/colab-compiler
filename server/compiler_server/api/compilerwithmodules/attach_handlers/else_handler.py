from ..utils import logger

def handle_else(node, ast, module_stack, block_stack):
    if block_stack and block_stack[-1].type == 'IF':
        block_stack.pop()
    if block_stack:
        block_stack[-1].children.append(node)
        block_stack.append(node)
        logger.debug("[Parser] Aninhado ELSE no bloco ativo e empilhado: %s", str(node))