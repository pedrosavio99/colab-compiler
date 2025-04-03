from .parsers.print_parser import parse_print
from .parsers.var_parser import parse_var
from .parsers.module_parser import parse_module_start, parse_module_end
from .parsers.initial_parser import parse_initial_start, parse_block_start, parse_block_end
from .utils import logger
from .ast import ASTNode  # Importar de ast.py

PARSER_DISPATCH = {
    'PRINT': parse_print,
    'VAR_DECL': parse_var,
    'MODULE_START': parse_module_start,
    'MODULE_END': parse_module_end,
    'INITIAL_START': parse_initial_start,
    'BLOCK_START': parse_block_start,
    'BLOCK_END': parse_block_end
}

def syslog_parse(tokens):
    logger.debug("[Parser][syslog_parse] Iniciando parsing dos tokens: %s", tokens)
    ast = []
    module_stack = []
    block_stack = []

    for token in tokens:
        token_type = token['type']
        parser_func = PARSER_DISPATCH.get(token_type)
        if parser_func:
            node = parser_func(token, module_stack if token_type in ('MODULE_START', 'MODULE_END') else block_stack)
            if node:
                if module_stack and token_type not in ('MODULE_END', 'BLOCK_START', 'BLOCK_END'):
                    module_stack[-1].children.append(node)
                elif block_stack and token_type not in ('MODULE_END', 'BLOCK_END'):
                    block_stack[-1].children.append(node)
                else:
                    ast.append(node)
            if token_type == 'BLOCK_START' and block_stack:
                block_stack.append(block_stack[-1])
            elif token_type == 'BLOCK_END' and block_stack:
                block_stack.pop()
        else:
            logger.warning("[Parser][syslog_parse] Tipo de token não suportado: %s", token_type)

    logger.debug("[Parser][syslog_parse] Finalizando parsing com AST: %s", [str(node) for node in ast])
    return ast