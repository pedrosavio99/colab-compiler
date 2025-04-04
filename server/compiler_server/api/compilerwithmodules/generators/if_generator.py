from ..utils import logger
from ..dispatch import GENERATOR_DISPATCH

def generate_if(node):
    logger.debug("[IfGenerator][generate_if] Processando nó: %s", str(node))
    condition = node.value['condition'].replace(' ', '')
    condition = condition.replace('in_data', 'self.in_data.value')
    code = [f"if {condition}:"]
    if_code = []
    else_code = []
    for child in node.children:
        gen_func = GENERATOR_DISPATCH.get(child.type)
        if gen_func:
            child_code = gen_func(child)
            if child.type in ('ASSIGN', 'PRINT') and not else_code:  # Primeiro bloco é o if
                if_code.extend([f"    {line}" for line in child_code])
            else:  # Segundo bloco é o else
                else_code.extend([f"    {line}" for line in child_code])
    code.extend(if_code)
    if else_code:
        code.append("else:")
        code.extend(else_code)
    logger.debug("[IfGenerator][generate_if] Código gerado: %s", code)
    return code

def generate_else(node):
    logger.debug("[IfGenerator][generate_else] Processando nó: %s", str(node))
    code = ["else:"]
    for child in node.children:
        gen_func = GENERATOR_DISPATCH.get(child.type)
        if gen_func:
            child_code = gen_func(child)
            code.extend([f"    {line}" for line in child_code])
    return code