from ..utils import logger

def generate_assign(node, indent_level=0):
    logger.debug("[AssignGenerator][generate_assign] Processando nó: %s, nível: %d", str(node), indent_level)
    indent = "    " * indent_level
    name = node.value['name']
    expr = node.value['expr'].replace('in_data', 'self.in_data.value')
    code = [f"{indent}self.{name}.set_value({expr})"]
    logger.debug("[AssignGenerator][generate_assign] Código gerado: %s", code)
    return code
