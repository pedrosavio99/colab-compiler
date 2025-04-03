# your_app/compilerwithmodules/handlers/module_handler.py
from ..utils import generate_unique_id, logger

def process_module(line):
    """Processa module e endmodule."""
    logger.debug("[ModuleHandler][process_module] Entrando na função para linha: %s", line)
    if line.startswith('module'):
        logger.debug("[ModuleHandler][process_module] Processando: identificado module")
        name = line.split()[1].strip(';')
        token = {'type': 'MODULE_START', 'name': name, 'id': generate_unique_id()}
        logger.debug("[ModuleHandler][process_module] Saindo com token: %s", token)
        return token
    elif line.startswith('endmodule'):
        logger.debug("[ModuleHandler][process_module] Processando: identificado endmodule")
        token = {'type': 'MODULE_END', 'id': generate_unique_id()}
        logger.debug("[ModuleHandler][process_module] Saindo com token: %s", token)
        return token
    logger.debug("[ModuleHandler][process_module] Saindo sem ação para linha: %s", line)
    return None