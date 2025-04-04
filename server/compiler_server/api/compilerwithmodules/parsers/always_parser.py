from ..utils import logger
from ..ast import ASTNode

def parse_always_posedge(token, block_stack):
    logger.debug("[AlwaysParser][parse_always_posedge] Processando token: %s", token)
    node = ASTNode('ALWAYS_POSEDGE', {'signal': token['signal']}, token['id'])
    block_stack.append(node)  # Empilha como um bloco
    logger.debug("[AlwaysParser][parse_always_posedge] Nó criado: %s", str(node))
    return node  # Retorna o nó ALWAYS_POSEDGE