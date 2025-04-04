from ..utils import logger
from ..dispatch import GENERATOR_DISPATCH

def generate_always_posedge(node):
    logger.debug("[AlwaysGenerator][generate_always_posedge] Processando nó: %s", str(node))
    signal = node.value.get('signal', 'clk')
    code = [
        f"    def update_always(self):",
        f"        # Sensível a posedge {signal}",
        f"        if self.{signal}.value and not self.{signal}.prev_value:  # Borda positiva"
    ]
    
    indent_level = "            "  # 12 espaços para alinhar com a borda positiva
    for child in node.children:
        gen_func = GENERATOR_DISPATCH.get(child.type)
        if gen_func:
            child_code = gen_func(child)
            logger.debug("[AlwaysGenerator] Gerando código para filho %s: %s", child.type, child_code)
            code.extend([f"{indent_level}{line}" for line in child_code])
        else:
            logger.warning("[AlwaysGenerator] Tipo de nó não suportado: %s", child.type)
    
    code.append(f"        self.{signal}.prev_value = self.{signal}.value")
    logger.debug("[AlwaysGenerator][generate_always_posedge] Código gerado: %s", code)
    return code