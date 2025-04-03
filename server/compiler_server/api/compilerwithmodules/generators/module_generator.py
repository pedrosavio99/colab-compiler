from ..utils import logger
from ..dispatch import GENERATOR_DISPATCH

def generate_module(node):
    logger.debug("[ModuleGenerator][generate_module] Processando nó: %s", str(node))
    code = [f"# Module: {node.value['name']} (ID: {node.id})"]
    for child in node.children:
        generator_func = GENERATOR_DISPATCH.get(child.type)
        if generator_func:
            child_code = generator_func(child)
            code.extend(child_code)
    code.append(f"# End of module: {node.value['name']}")
    logger.debug("[ModuleGenerator][generate_module] Código gerado: %s", code)
    return code