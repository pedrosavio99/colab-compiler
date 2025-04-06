from ..utils import logger

def handle_always_posedge(node, ast, module_stack, block_stack):
    if module_stack:
        module_stack[-1].children.append(node)
        block_stack.append(node)
        logger.debug("[Parser] Aninhado ALWAYS_POSEDGE no MODULE e block_stack: %s", str(node))