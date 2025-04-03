from .dispatch import GENERATOR_DISPATCH, initialize_generator_dispatch
from .utils import logger

def generate_python(ast):
    logger.debug("[Generator][generate_python] Iniciando geração de código Python para AST: %s", [str(node) for node in ast])
    # Inicializa o dispatch na primeira execução
    if not GENERATOR_DISPATCH:
        initialize_generator_dispatch()
    
    py_code = []
    imports = ["from sys import argv"]

    for node in ast:
        node_type = node.type
        generator_func = GENERATOR_DISPATCH.get(node_type)
        if generator_func:
            code_lines = generator_func(node)
            py_code.extend(code_lines)
        else:
            logger.warning("[Generator][generate_python] Tipo de nó não suportado: %s", node_type)

    final_code = '\n'.join(imports + py_code)
    logger.debug("[Generator][generate_python] Finalizando geração com código: %s", final_code)
    return final_code