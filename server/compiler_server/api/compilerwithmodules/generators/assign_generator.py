from ..utils import logger

def generate_assign(node):
    """Gera código Python para atribuições."""
    logger.debug("[AssignGenerator][generate_assign] Processando nó: %s", str(node))
    name = node.value['name']
    expr = node.value['expr'].replace(' ', '')  # Ex: "in_data+1"
    expr = expr.replace('in_data', 'self.in_data.value')  # Ajusta para atributos
    code = [f"self.{name}.set_value({expr})"]
    return code