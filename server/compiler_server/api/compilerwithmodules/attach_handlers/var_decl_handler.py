from ..utils import logger

def handle_var_decl(node, ast, module_stack, block_stack):
    if block_stack:
        block_stack[-1].children.append(node)
        logger.debug("[Parser] Aninhado VAR_DECL no bloco ativo: %s", str(node))
    elif module_stack:
        module_stack[-1].children.append(node)
        logger.debug("[Parser] Aninhado VAR_DECL no MODULE: %s", str(node))
    else:
        ast.append(node)
        logger.debug("[Parser] Adicionado VAR_DECL à AST (fora de módulo): %s", str(node))