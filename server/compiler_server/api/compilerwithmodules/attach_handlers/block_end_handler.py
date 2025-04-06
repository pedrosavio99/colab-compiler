from ..utils import logger

def handle_block_end(node, ast, module_stack, block_stack):
    if block_stack:
        block_stack.pop()
        logger.debug("[Parser] Bloco fechado, block_stack: %s", [str(n) for n in block_stack])