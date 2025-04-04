from ..utils import generate_unique_id, logger
import re

def process_if(line):
    """Processa instruções if e else."""
    logger.debug("[IfHandler][process_if] Processando linha: %s", line)
    if_match = re.match(r'if\s*\(([^)]+)\)\s*begin', line.strip())
    if if_match:
        condition = if_match.group(1)
        token = {'type': 'IF', 'condition': condition, 'id': generate_unique_id()}
        logger.debug("[IfHandler][process_if] Token IF gerado: %s", token)
        return token
    elif line.strip() == 'end else begin':
        token = {'type': 'ELSE', 'id': generate_unique_id()}
        logger.debug("[IfHandler][process_if] Token ELSE gerado: %s", token)
        return token
    return None