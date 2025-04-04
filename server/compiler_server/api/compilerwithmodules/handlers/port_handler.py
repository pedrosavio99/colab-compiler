from ..utils import generate_unique_id, logger
import re

def process_port(line):
    """Processa declarações de portas (input/output logic)."""
    logger.debug("[PortHandler][process_port] Processando linha: %s", line)
    match = re.match(r'(input|output)\s+logic\s+(?:\[(\d+):(\d+)\])?\s*(\w+)', line.strip())
    if match:
        direction, msb, lsb, name = match.groups()
        width = int(msb) - int(lsb) + 1 if msb and lsb else None
        token = {
            'type': 'PORT',
            'direction': direction,
            'name': name,
            'width': width,
            'id': generate_unique_id()
        }
        logger.debug("[PortHandler][process_port] Token gerado: %s", token)
        return token
    return None