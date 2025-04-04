from ..utils import logger
from ..dispatch import GENERATOR_DISPATCH

def generate_module(node):
    logger.debug("[ModuleGenerator][generate_module] Processando nó: %s", str(node))
    code = [f"# Module: {node.value['name']} (ID: {node.id})"]
    
    # Verifica se há portas ou blocos always para incluir a classe Signal
    has_ports_or_always = any(child.type in ['PORT', 'ALWAYS_POSEDGE'] for child in node.children)
    if has_ports_or_always:
        code.extend([
            "from sys import argv",
            "",
            "class Signal:",
            "    def __init__(self, value=0, width=None):",
            "        self.value = value",
            "        self.width = width",
            "        self.prev_value = value",
            "    def set_value(self, value):",
            "        if self.width:",
            "            self.value = value & ((1 << self.width) - 1)",
            "        else:",
            "            self.value = value",
            "",
            f"class {node.value['name']}:",
            "    def __init__(self):"
        ])
    else:
        code.insert(0, "from sys import argv")  # Apenas para módulos simples
    
    # Processa os filhos
    port_lines = []
    always_lines = []
    other_lines = []
    
    for child in node.children:
        logger.debug("[ModuleGenerator] Processando filho: %s", str(child))
        generator_func = GENERATOR_DISPATCH.get(child.type)
        if generator_func:
            child_code = generator_func(child)
            if child.type == 'PORT' and has_ports_or_always:
                port_lines.extend(child_code)
            elif child.type == 'ALWAYS_POSEDGE' and has_ports_or_always:
                always_lines.extend(child_code)
            else:
                other_lines.extend(child_code)
        else:
            logger.warning("[ModuleGenerator] Tipo de nó não suportado: %s", child.type)
    
    # Adiciona as portas ao __init__
    if port_lines:
        code.extend([f"        {line}" for line in port_lines])
    
    # Adiciona os blocos always como métodos
    if always_lines:
        code.extend([""])  # Linha em branco antes do método
        code.extend(always_lines)
    
    # Adiciona o método run() apenas se houver portas ou always
    if has_ports_or_always:
        code.extend([
            "",
            "    def run(self, clk_value, in_data_value):",
            "        self.clk.set_value(clk_value)",
            "        self.in_data.set_value(in_data_value)",
            "        self.update_always()",
            "        return self.out_data.value"
        ])
    
    # Adiciona outros códigos (como PRINT fora de always)
    if other_lines:
        code.extend(other_lines)
    
    code.append(f"# End of module: {node.value['name']}")
    logger.debug("[ModuleGenerator][generate_module] Código gerado: %s", code)
    return code