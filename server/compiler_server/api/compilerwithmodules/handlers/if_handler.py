from ..utils import generate_unique_id, logger
import re

def process_if(line):
    """Processa instruções if e else."""
    logger.debug("[IfHandler][process_if] Processando linha: %s", line)
    # Remove comentários para simplificar a análise
    line_without_comments = re.sub(r'//.*$', '', line).strip()
    
    # Checa o 'if'
    if_match = re.match(r'if\s*\(([^)]+)\)\s*begin', line_without_comments, re.IGNORECASE)
    if if_match:
        condition = if_match.group(1)
        token = {'type': 'IF', 'condition': condition, 'id': generate_unique_id()}
        logger.debug("[IfHandler][process_if] Token IF gerado: %s", token)
        return token
    
    # Checa o 'else'
    else_match = re.match(r'end\s+else\s+begin', line_without_comments, re.IGNORECASE)
    if else_match:
        token = {'type': 'ELSE', 'id': generate_unique_id()}
        logger.debug("[IfHandler][process_if] Token ELSE gerado: %s", token)
        return token
    
    return None