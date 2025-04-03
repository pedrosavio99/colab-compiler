from ..utils import logger
from ..ast import ASTNode

def parse_print(token, module_stack):
    logger.debug("[PrintParser][parse_print] Processando token: %s", token)
    node = ASTNode('PRINT', {'message': token['message'], 'var': token['var']}, token['id'])
    logger.debug("[PrintParser][parse_print] Nó criado: %s", str(node))
    return node