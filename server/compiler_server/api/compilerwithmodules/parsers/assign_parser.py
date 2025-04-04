from ..utils import logger
from ..ast import ASTNode

def parse_assign(token, block_stack):
    logger.debug("[AssignParser][parse_assign] Processando token: %s", token)
    node = ASTNode('ASSIGN', {'name': token['name'], 'expr': token['expr']}, token['id'])
    logger.debug("[AssignParser][parse_assign] Nó criado: %s", str(node))
    return node