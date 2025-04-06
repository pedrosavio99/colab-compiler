from ..utils import logger

def handle_module_start(node, ast, module_stack, block_stack):
    ast.append(node)
    module_stack.append(node)
    logger.debug("[Parser] Adicionado MODULE à AST: %s", str(node))