from ..utils import logger

def generate_print(node):
    """Gera código Python para o nó PRINT."""
    logger.debug("[PrintGenerator][generate_print] Processando nó: %s", str(node))
    message = node.value['message']
    var = node.value['var']
    if var:
        code = [f'print("{message}".format(self.{var}.value))']
    else:
        code = [f'print("{message}")']
    logger.debug("[PrintGenerator][generate_print] Código gerado: %s", code)
    return code