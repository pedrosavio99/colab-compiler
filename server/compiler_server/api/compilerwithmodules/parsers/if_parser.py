from ..utils import logger
from ..ast import ASTNode

def parse_if(token, block_stack):
    logger.debug("[IfParser][parse_if] Processando token: %s", token)
    node = ASTNode('IF', {'condition': token['condition']}, token['id'])
    logger.debug("[IfParser][parse_if] Nó criado: %s", str(node))
    return node

def parse_else(token, block_stack):
    logger.debug("[IfParser][parse_else] Processando token: %s", token)
    node = ASTNode('ELSE', {}, token['id'])
    logger.debug("[IfParser][parse_else] Nó criado: %s", str(node))
    return node