from ..utils import generate_unique_id, logger
import re

def process_var(line):
    logger.debug("[VarHandler][process_var] Processando linha: %s", line)
    var_match = re.match(r'reg\s+(?:\[(\d+):(\d+)\])?\s*(\w+)\s*=\s*(\d+)', line)
    if var_match:
        msb, lsb, name, value = var_match.groups()
        width = int(msb) - int(lsb) + 1 if msb and lsb else None
        token = {'type': 'VAR_DECL', 'name': name, 'width': width, 'value': int(value), 'id': generate_unique_id()}
        logger.debug("[VarHandler][process_var] Token gerado: %s", token)
        return token
    assign_match = re.match(r'(\w+)\s*<=?\s*([^;]+);', line.strip())
    if assign_match:
        name, expr = assign_match.groups()
        token = {'type': 'ASSIGN', 'name': name, 'expr': expr.strip(), 'id': generate_unique_id()}
        logger.debug("[VarHandler][process_var] Token ASSIGN gerado: %s", token)
        return token
    return None