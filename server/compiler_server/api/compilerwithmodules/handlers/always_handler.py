from ..utils import generate_unique_id, logger
import re

def process_always(line):
    """Processa blocos always com sensibilidade a borda."""
    logger.debug("[AlwaysHandler][process_always] Processando linha: %s", line)
    match = re.match(r'always\s+@\(posedge\s+(\w+)\)\s+begin', line.strip())
    if match:
        signal = match.group(1)
        token = {
            'type': 'ALWAYS_POSEDGE',
            'signal': signal,
            'id': generate_unique_id()
        }
        logger.debug("[AlwaysHandler][process_always] Token gerado: %s", token)
        return token
    return None