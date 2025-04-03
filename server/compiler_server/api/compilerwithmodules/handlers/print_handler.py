from ..utils import generate_unique_id, logger
import re

def process_print(line):
    logger.debug("[PrintHandler][process_print] Entrando na função para linha: %s", line)
    # Ajuste na regex: captura toda a string entre aspas como message, e var só se for um identificador válido após vírgula
    match = re.match(r'\$display\s*\("([^"]*)"(?:\s*,\s*(\w+))?\s*\)\s*;', line)
    if match:
        message, var = match.groups()
        token = {'type': 'PRINT', 'message': message, 'var': var, 'id': generate_unique_id()}
        logger.debug("[PrintHandler][process_print] Token gerado: %s", token)
        return token
    logger.debug("[PrintHandler][process_print] Saindo sem ação para linha: %s", line)
    return None