from ..utils import logger
from ..ast import ASTNode

def parse_initial_start(token, module_stack):
    logger.debug("[InitialParser][parse_initial_start] Processando token: %s", token)
    node = ASTNode('INITIAL', {}, token['id'])
    logger.debug("[InitialParser][parse_initial_start] Nó criado: %s", str(node))
    return node

def parse_block_start(token, module_stack):
    logger.debug("[InitialParser][parse_block_start] Processando token: %s", token)
    return None

def parse_block_end(token, module_stack):
    logger.debug("[InitialParser][parse_block_end] Processando token: %s", token)
    return None