from .handlers.print_handler import process_print
from .handlers.var_handler import process_var
from .handlers.module_handler import process_module
from .handlers.initial_handler import process_initial
from .utils import logger

handlers = [
    process_print,
    process_var,
    process_module,
    process_initial
]

def syslog_lexer(code):
    logger.debug("[Lexer][syslog_lexer] Iniciando tokenização do código")
    tokens = []
    lines = code.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        for handler in handlers:
            token = handler(line)
            if token:
                tokens.append(token)
                break
        else:
            logger.warning("[Lexer][syslog_lexer] Linha não reconhecida: %s", line)
    logger.debug("[Lexer][syslog_lexer] Finalizando tokenização com tokens: %s", tokens)
    return tokens