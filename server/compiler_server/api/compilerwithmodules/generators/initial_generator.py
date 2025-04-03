from ..utils import logger
from ..dispatch import GENERATOR_DISPATCH

def generate_initial(node):
    logger.debug("[InitialGenerator][generate_initial] Processando nó: %s", str(node))
    code = ["# Initial block"]
    for child in node.children:
        generator_func = GENERATOR_DISPATCH.get(child.type)
        if generator_func:
            child_code = generator_func(child)
            code.extend(child_code)
    logger.debug("[InitialGenerator][generate_initial] Código gerado: %s", code)
    return code