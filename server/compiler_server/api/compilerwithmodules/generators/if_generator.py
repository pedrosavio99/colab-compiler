from ..utils import logger
from ..dispatch import GENERATOR_DISPATCH

def generate_if(node, indent_level=0):
    logger.debug("[IfGenerator] Arquivo carregado com sucesso na inicialização")
    logger.debug("[IfGenerator][generate_if] Processando nó: %s, nível: %d", str(node), indent_level)
    condition = node.value['condition'].replace(' ', '')
    condition = condition.replace('in_data', 'self.in_data.value')
    indent = "    " * indent_level
    code = [f"{indent}if {condition}:"]
    
    # Processa apenas os filhos diretos do IF
    for child in node.children:
        gen_func = GENERATOR_DISPATCH.get(child.type)
        if gen_func:
            logger.debug("[IfGenerator][generate_if] Chamando gerador para %s com nível: %d", child.type, indent_level + 1)
            child_code = gen_func(child, indent_level + 1)  # Nível + 1 para os filhos
            code.extend(child_code)
    
    logger.debug("[IfGenerator][generate_if] Código gerado: %s", code)
    return code

def generate_else(node, indent_level=0):
    logger.debug("[IfGenerator][generate_else] Processando nó: %s, nível: %d", str(node), indent_level)
    indent = "    " * indent_level
    code = [f"{indent}else:"]
    
    # Processa apenas os filhos diretos do ELSE
    for child in node.children:
        gen_func = GENERATOR_DISPATCH.get(child.type)
        if gen_func:
            logger.debug("[IfGenerator][generate_else] Chamando gerador para %s com nível: %d", child.type, indent_level + 1)
            child_code = gen_func(child, indent_level + 1)  # Nível + 1 para os filhos
            code.extend(child_code)
    
    logger.debug("[IfGenerator][generate_else] Código gerado: %s", code)
    return code