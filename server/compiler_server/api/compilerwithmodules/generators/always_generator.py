from ..utils import logger
from ..dispatch import GENERATOR_DISPATCH

def generate_always_posedge(node, indent_level=1):
    logger.debug("[AlwaysGenerator][generate_always_posedge] Processando nó: %s, nível: %d", str(node), indent_level)
    signal = node.value.get('signal', 'clk')
    indent = "    " * indent_level
    indent_inner = "    " * (indent_level + 1)  # Nível 2 pro primeiro if
    code = [
        f"{indent}def update_always(self):",
        f"{indent_inner}# Sensível a posedge {signal}",
        f"{indent_inner}if self.{signal}.value and not self.{signal}.prev_value:  # Borda positiva"
    ]
    
    # Processa os filhos do ALWAYS_POSEDGE com nível maior
    for child in node.children:
        gen_func = GENERATOR_DISPATCH.get(child.type)
        if gen_func:
            child_code = gen_func(child, indent_level + 2)  # Nível 3 pro IF/ELSE
            code.extend(child_code)
        else:
            logger.warning("[AlwaysGenerator] Tipo de nó não suportado: %s", child.type)
    
    code.append(f"{indent_inner}self.{signal}.prev_value = self.{signal}.value")
    logger.debug("[AlwaysGenerator][generate_always_posedge] Código gerado: %s", code)
    return code