# dispatch.py

GENERATOR_DISPATCH = {}

def initialize_generator_dispatch():
    """Inicializa o GENERATOR_DISPATCH com os geradores necessários."""
    from .generators.print_generator import generate_print
    from .generators.var_generator import generate_var
    from .generators.module_generator import generate_module
    from .generators.initial_generator import generate_initial
    from .generators.always_generator import generate_always_posedge
    from .generators.assign_generator import generate_assign
    from .generators.if_generator import generate_else, generate_if
    from .generators.port_generator import generate_port

    GENERATOR_DISPATCH.update({
        'PRINT': generate_print,
        'VAR_DECL': generate_var,
        'MODULE': generate_module,
        'INITIAL': generate_initial,
        'BLOCK': lambda node: [f"# Block (ID: {node.id})"],
        'PORT': generate_port,
        'ALWAYS_POSEDGE': generate_always_posedge,
        'IF': generate_if,
        'ELSE': generate_else,
        'ASSIGN': generate_assign
    })