from ..utils import logger

def generate_print(node):
    logger.debug("[PrintGenerator][generate_print] Processando nó: %s", str(node))
    message = node.value.get('message', '')  # Pega a mensagem do token
    var = node.value.get('var', None)        # Pega a variável, se existir
    
    # Constrói a string de saída
    if var:
        code = [f'print("{message}", {var})']  # Exemplo: print("Valor:", x)
    else:
        code = [f'print("{message}")']         # Exemplo: print("Hello, World!")
    
    logger.debug("[PrintGenerator][generate_print] Código gerado: %s", code)
    return code