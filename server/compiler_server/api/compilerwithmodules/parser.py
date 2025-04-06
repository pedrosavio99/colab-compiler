from .parsers.assign_parser import parse_assign
from .parsers.if_parser import parse_else, parse_if
from .parsers.always_parser import parse_always_posedge
from .parsers.port_parser import parse_port
from .parsers.print_parser import parse_print
from .parsers.var_parser import parse_var
from .parsers.module_parser import parse_module_start, parse_module_end
from .parsers.initial_parser import parse_initial_start, parse_block_start, parse_block_end
from .attach_handlers import (
    handle_module_start, handle_module_end, handle_always_posedge,
    handle_if, handle_else, handle_assign_print, handle_var_decl,
    handle_port, handle_initial_start, handle_block_start, handle_block_end
)
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
            context = module_stack if token_type in ('MODULE_START', 'MODULE_END') else block_stack
            node = parser_func(token, context)
            if node:
                attach_node(token_type, node, ast, module_stack, block_stack)
        else:
            logger.warning("[Parser][syslog_parse] Tipo de token não suportado: %s", token_type)

    logger.debug("[Parser][syslog_parse] Finalizando parsing com AST: %s", [str(n) for n in ast])
    return ast