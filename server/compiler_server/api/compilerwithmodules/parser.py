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
                if token_type == 'MODULE_START':
                    ast.append(node)
                    module_stack.append(node)
                    logger.debug("[Parser] Adicionado MODULE à AST: %s", str(node))
                elif token_type == 'MODULE_END':
                    if module_stack:
                        module_stack.pop()
                    if block_stack:
                        block_stack.clear()
                    logger.debug("[Parser] MODULE finalizado, AST atual: %s", [str(n) for n in ast])
                elif token_type == 'ALWAYS_POSEDGE':
                    if module_stack:
                        module_stack[-1].children.append(node)
                        block_stack.append(node)  # Inicia o bloco
                        logger.debug("[Parser] Aninhado ALWAYS_POSEDGE no MODULE e block_stack: %s", str(node))
                elif token_type == 'IF':
                    if block_stack:
                        block_stack[-1].children.append(node)
                        block_stack.append(node)  # Empilha o IF como bloco ativo
                        logger.debug("[Parser] Aninhado IF no bloco ativo e empilhado: %s", str(node))
                elif token_type == 'ELSE':
                    if block_stack and block_stack[-1].type == 'IF':
                        block_stack.pop()  # Fecha o IF
                    if block_stack:
                        block_stack[-1].children.append(node)
                        block_stack.append(node)  # Empilha o ELSE como bloco ativo
                        logger.debug("[Parser] Aninhado ELSE no bloco ativo e empilhado: %s", str(node))
                elif token_type in ('ASSIGN', 'PRINT'):
                    if block_stack:
                        block_stack[-1].children.append(node)
                        logger.debug("[Parser] Aninhado %s no bloco ativo: %s", token_type, str(node))
                    elif module_stack:
                        module_stack[-1].children.append(node)
                        logger.debug("[Parser] Aninhado %s no MODULE: %s", token_type, str(node))
                elif token_type == 'BLOCK_START':
                    pass  # Já tratado pelo parser específico, se necessário
                elif token_type == 'BLOCK_END':
                    if block_stack:
                        block_stack.pop()
                        logger.debug("[Parser] Bloco fechado, block_stack: %s", [str(n) for n in block_stack])
                elif block_stack:
                    block_stack[-1].children.append(node)
                    logger.debug("[Parser] Aninhado no bloco ativo: %s", str(node))
                elif module_stack:
                    module_stack[-1].children.append(node)
                    logger.debug("[Parser] Aninhado no MODULE: %s", str(node))
                else:
                    ast.append(node)
                    logger.debug("[Parser] Adicionado à AST (fora de módulo): %s", str(node))
        else:
            logger.warning("[Parser][syslog_parse] Tipo de token não suportado: %s", token_type)

    logger.debug("[Parser][syslog_parse] Finalizando parsing com AST: %s", [str(n) for n in ast])
    return ast