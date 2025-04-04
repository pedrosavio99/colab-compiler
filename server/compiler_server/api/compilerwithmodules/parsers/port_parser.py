from ..utils import logger
from ..ast import ASTNode

def parse_port(token, module_stack):
    """Transforma o token PORT em um nó da AST."""
    logger.debug("[PortParser][parse_port] Processando token: %s", token)
    node = ASTNode('PORT', {
        'direction': token['direction'],
        'name': token['name'],
        'width': token['width']
    }, token['id'])
    logger.debug("[PortParser][parse_port] Nó criado: %s", str(node))
    return node