from ..ast import ASTNode
from ..utils import logger

def parse_if(token, block_stack):
    if_node = ASTNode(type='IF', value={'condition': token['condition']}, id=token['id'], children=[])
    logger.debug("[IfParser][parse_if] Nó criado: %s", str(if_node))
    return if_node  # Retorna só o nó, sem mexer no block_stack

def parse_else(token, block_stack):
    else_node = ASTNode(type='ELSE', value={}, id=token['id'], children=[])
    logger.debug("[IfParser][parse_else] Nó criado: %s", str(else_node))
    return else_node  # Retorna só o nó, sem mexer no block_stack