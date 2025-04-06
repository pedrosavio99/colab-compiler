from .parsers.assign_parser import parse_assign
from .parsers.if_parser import parse_else, parse_if
from .parsers.always_parser import parse_always_posedge
from .parsers.port_parser import parse_port
from .parsers.print_parser import parse_print
from .parsers.var_parser import parse_var
from .parsers.module_parser import parse_module_start, parse_module_end
from .parsers.initial_parser import parse_initial_start, parse_block_start, parse_block_end
from .utils import logger
from .ast import ASTNode

PARSER_DISPATCH = {
    'PRINT': parse_print,
    'VAR_DECL': parse_var,
    'MODULE_START': parse_module_start,
    'MODULE_END': parse_module_end,
    'INITIAL_START': parse_initial_start,
    'BLOCK_START': parse_block_start,
    'BLOCK_END': parse_block_end,
    'PORT': parse_port,
    'ALWAYS_POSEDGE': parse_always_posedge,
    'IF': parse_if,
    'ELSE': parse_else,
    'ASSIGN': parse_assign
}


# Funções de encaixe na AST
def handle_module_start(node, ast, module_stack, block_stack):
    ast.append(node)
    module_stack.append(node)
    logger.debug("[Parser] Adicionado MODULE à AST: %s", str(node))


def handle_module_end(node, ast, module_stack, block_stack):
    if module_stack:
        module_stack.pop()
    if block_stack:
        block_stack.clear()
    logger.debug("[Parser] MODULE finalizado, AST atual: %s", [str(n) for n in ast])


def handle_always_posedge(node, ast, module_stack, block_stack):
    if module_stack:
        module_stack[-1].children.append(node)
        block_stack.append(node)  # Inicia o bloco
        logger.debug("[Parser] Aninhado ALWAYS_POSEDGE no MODULE e block_stack: %s", str(node))


def handle_if(node, ast, module_stack, block_stack):
    if block_stack:
        block_stack[-1].children.append(node)
        block_stack.append(node)  # Empilha o IF como bloco ativo
        logger.debug("[Parser] Aninhado IF no bloco ativo e empilhado: %s", str(node))


def handle_else(node, ast, module_stack, block_stack):
    if block_stack and block_stack[-1].type == 'IF':
        block_stack.pop()  # Fecha o IF
    if block_stack:
        block_stack[-1].children.append(node)
        block_stack.append(node)  # Empilha o ELSE como bloco ativo
        logger.debug("[Parser] Aninhado ELSE no bloco ativo e empilhado: %s", str(node))


def handle_assign_print(node, ast, module_stack, block_stack):
    if block_stack:
        block_stack[-1].children.append(node)
        logger.debug("[Parser] Aninhado %s no bloco ativo: %s", node.type, str(node))
    elif module_stack:
        module_stack[-1].children.append(node)
        logger.debug("[Parser] Aninhado %s no MODULE: %s", node.type, str(node))
    else:
        ast.append(node)
        logger.debug("[Parser] Adicionado %s à AST (fora de módulo): %s", node.type, str(node))


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


def handle_port(node, ast, module_stack, block_stack):
    if block_stack:
        block_stack[-1].children.append(node)
        logger.debug("[Parser] Aninhado PORT no bloco ativo: %s", str(node))
    elif module_stack:
        module_stack[-1].children.append(node)
        logger.debug("[Parser] Aninhado PORT no MODULE: %s", str(node))
    else:
        ast.append(node)
        logger.debug("[Parser] Adicionado PORT à AST (fora de módulo): %s", str(node))


def handle_initial_start(node, ast, module_stack, block_stack):
    if block_stack:
        block_stack[-1].children.append(node)
        logger.debug("[Parser] Aninhado INITIAL_START no bloco ativo: %s", str(node))
    elif module_stack:
        module_stack[-1].children.append(node)
        logger.debug("[Parser] Aninhado INITIAL_START no MODULE: %s", str(node))
    else:
        ast.append(node)
        logger.debug("[Parser] Adicionado INITIAL_START à AST (fora de módulo): %s", str(node))


def handle_block_start(node, ast, module_stack, block_stack):
    # Já é tratado pelo parser específico, se necessário.
    pass


def handle_block_end(node, ast, module_stack, block_stack):
    if block_stack:
        block_stack.pop()
        logger.debug("[Parser] Bloco fechado, block_stack: %s", [str(n) for n in block_stack])


# Dicionário para despacho das funções de encaixe
ATTACH_HANDLERS = {
    'MODULE_START': handle_module_start,
    'MODULE_END': handle_module_end,
    'ALWAYS_POSEDGE': handle_always_posedge,
    'IF': handle_if,
    'ELSE': handle_else,
    'ASSIGN': handle_assign_print,
    'PRINT': handle_assign_print,
    'VAR_DECL': handle_var_decl,
    'PORT': handle_port,
    'INITIAL_START': handle_initial_start,
    'BLOCK_START': handle_block_start,
    'BLOCK_END': handle_block_end,
}


def attach_node(token_type, node, ast, module_stack, block_stack):
    handler = ATTACH_HANDLERS.get(token_type)
    if handler:
        handler(node, ast, module_stack, block_stack)
    else:
        if block_stack:
            block_stack[-1].children.append(node)
            logger.debug("[Parser] Aninhado no bloco ativo: %s", str(node))
        elif module_stack:
            module_stack[-1].children.append(node)
            logger.debug("[Parser] Aninhado no MODULE: %s", str(node))
        else:
            ast.append(node)
            logger.debug("[Parser] Adicionado à AST (fora de módulo): %s", str(node))


def syslog_parse(tokens):
    logger.debug("[Parser][syslog_parse] Iniciando parsing dos tokens: %s", tokens)
    ast = []
    module_stack = []
    block_stack = []

    for token in tokens:
        token_type = token['type']
        parser_func = PARSER_DISPATCH.get(token_type)
        if parser_func:
            # Usa module_stack para MODULE_START e MODULE_END; caso contrário, usa block_stack.
            context = module_stack if token_type in ('MODULE_START', 'MODULE_END') else block_stack
            node = parser_func(token, context)
            if node:
                attach_node(token_type, node, ast, module_stack, block_stack)
        else:
            logger.warning("[Parser][syslog_parse] Tipo de token não suportado: %s", token_type)

    logger.debug("[Parser][syslog_parse] Finalizando parsing com AST: %s", [str(n) for n in ast])
    return ast
