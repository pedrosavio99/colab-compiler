# your_app/compilerwithmodules/generators/var_generator.py
from ..utils import logger

def generate_var(node):
    """Gera código Python para nó VAR_DECL."""
    logger.debug("[VarGenerator][generate_var] Processando nó: %s", str(node))
    code = [f"{node.value['name']} = 0  # {node.value['width']}-bit variable"]
    logger.debug("[VarGenerator][generate_var] Código gerado: %s", code)
    return code