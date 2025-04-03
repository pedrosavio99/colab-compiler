from ..utils import logger
from ..ast import ASTNode

def parse_var(token, module_stack):
    logger.debug("[VarParser][parse_var] Processando token: %s", token)
    node = ASTNode('VAR_DECL', {'width': token['width'], 'name': token['name']}, token['id'])
    logger.debug("[VarParser][parse_var] Nó criado: %s", str(node))
    return node