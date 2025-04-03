from ..utils import generate_unique_id, logger
import re

def process_initial(line):
    """Processa initial, begin e end no código SystemVerilog."""
    logger.debug("[InitialHandler][process_initial] Processando linha: %s", line)
    
    # Match para 'initial'
    if re.match(r'^\s*initial\s*$', line):
        token = {'type': 'INITIAL_START', 'id': generate_unique_id()}
        logger.debug("[InitialHandler][process_initial] Token INITIAL_START gerado: %s", token)
        return token
    
    # Match para 'begin'
    elif re.match(r'^\s*begin\s*$', line):
        token = {'type': 'BLOCK_START', 'id': generate_unique_id()}
        logger.debug("[InitialHandler][process_initial] Token BLOCK_START gerado: %s", token)
        return token
    
    # Match para 'end'
    elif re.match(r'^\s*end\s*$', line):
        token = {'type': 'BLOCK_END', 'id': generate_unique_id()}
        logger.debug("[InitialHandler][process_initial] Token BLOCK_END gerado: %s", token)
        return token
    
    logger.debug("[InitialHandler][process_initial] Nenhuma correspondência para linha: %s", line)
    return None