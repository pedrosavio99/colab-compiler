from ..utils import logger

def generate_print(node, indent_level=0):
    logger.debug("[PrintGenerator][generate_print] Processando nó: %s, nível: %d", str(node), indent_level)
    indent = "    " * indent_level
    message = node.value['message']
    var = node.value.get('var')
    if var:
        code = [f"{indent}print(\"{message}\".format(self.{var}.value))"]
    else:
        code = [f"{indent}print(\"{message}\")"]
    logger.debug("[PrintGenerator][generate_print] Código gerado: %s", code)
    return code