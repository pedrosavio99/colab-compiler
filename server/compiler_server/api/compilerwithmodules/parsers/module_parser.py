from ..utils import logger
from ..ast import ASTNode

def parse_module_start(token, module_stack):
    logger.debug("[ModuleParser][parse_module_start] Processando token: %s", token)
    node = ASTNode('MODULE', {'name': token['name']}, token['id'])
    module_stack.append(node)
    logger.debug("[ModuleParser][parse_module_start] Nó criado e empilhado: %s", str(node))
    return None

def parse_module_end(token, module_stack):
    logger.debug("[ModuleParser][parse_module_end] Processando token: %s", token)
    if module_stack:
        node = module_stack.pop()
        logger.debug("[ModuleParser][parse_module_end] Nó finalizado: %s", str(node))
        return node
    logger.warning("[ModuleParser][parse_module_end] Pilha vazia, nenhum módulo para fechar")
    return None