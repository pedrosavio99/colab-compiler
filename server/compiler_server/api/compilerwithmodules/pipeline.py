from .lexer import syslog_lexer
from .parser import syslog_parse
from .generator import generate_python
from .utils import logger

def run_compiler_pipeline(code):
    logger.info("Iniciando pipeline de compilação...")
    tokens = syslog_lexer(code)
    logger.info("Tokens gerados: %s", tokens)
    ast = syslog_parse(tokens)
    logger.info("AST gerada: %s", [str(node) for node in ast])
    python_code = generate_python(ast)
    logger.info("Código Python gerado: %s", python_code)
    return {
        "tokens": tokens,
        "ast": [str(node) for node in ast],
        "python": python_code
    }