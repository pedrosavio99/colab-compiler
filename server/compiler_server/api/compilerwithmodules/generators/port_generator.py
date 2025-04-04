from ..utils import logger

def generate_port(node):
    """Gera código Python para portas."""
    logger.debug("[PortGenerator][generate_port] Processando nó: %s", str(node))
    name = node.value['name']
    width = node.value['width']
    direction = node.value['direction']
    code = [f"self.{name} = Signal(0, {width if width else 'None'})  # {direction} logic"]
    return code