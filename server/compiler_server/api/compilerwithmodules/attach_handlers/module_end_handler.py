from ..utils import logger

def handle_module_end(node, ast, module_stack, block_stack):
    if module_stack:
        module_stack.pop()
    if block_stack:
        block_stack.clear()
    logger.debug("[Parser] MODULE finalizado, AST atual: %s", [str(n) for n in ast])