# your_app/compilerwithmodules/handlers/var_handler.py
import re
from ..utils import generate_unique_id, logger

def process_var(line):
    """Processa declarações de variáveis."""
    logger.debug("[VarHandler][process_var] Entrando na função para linha: %s", line)
    if re.match(r'reg\s*\[\d+:\d+\]\s*\w+;', line):
        logger.debug("[VarHandler][process_var] Processando: identificado reg")
        bits = re.search(r'\[(\d+):(\d+)\]', line)
        width = int(bits.group(1)) - int(bits.group(2)) + 1
        name = re.search(r'\w+;', line).group(0)[:-1]
        token = {'type': 'VAR_DECL', 'width': width, 'name': name, 'id': generate_unique_id()}
        logger.debug("[VarHandler][process_var] Saindo com token: %s", token)
        return token
    logger.debug("[VarHandler][process_var] Saindo sem ação para linha: %s", line)
    return None