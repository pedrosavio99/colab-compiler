from .systemverilog import SystemVerilogGenerator as SVGen
from .utils import check_for_string_op

class SystemVerilogGenerator(SVGen):
    def __init__(self):
        super().__init__()
        self.main_signals = []
        self.main_instances = []
        self.display_statements = []  # Para armazenar os $display

    def visit(self, node):
        if check_for_string_op(node):
            raise ValueError("Erro: Operações com strings não são permitidas.")
        if node.type == 'program':
            return self.visit_program(node)
        elif node.type == 'assignment':
            self.visit_assignment(node)
        elif node.type == 'if':
            self.visit_if(node)
        elif node.type == 'for':
            self.visit_for(node)
        elif node.type == 'while':
            self.visit_while(node)
        elif node.type == 'function':
            self.visit_function(node)
        elif node.type == 'print':
            self.visit_print(node)
        else:
            raise ValueError(f"Erro: '{node.type}' não é permitido.")

    def visit_program(self, node):
        self.main_signals = []
        self.main_instances = []
        self.display_statements = []
        for child in node.children:
            self.visit(child)
        code = ["module main;"]
        code.extend(self.main_signals)
        code.extend(self.main_instances)
        if self.display_statements:
            code.append("    initial begin")
            code.extend([f"        {stmt}" for stmt in self.display_statements])
            code.append("    end")
        code.append("endmodule")
        return "\n".join(code)

    def visit_assignment(self, node):
        identifier = node.children[0].value
        expr_type, expr_value = self.visit_expression(node.children[1])
        self.main_signals.append(f"{expr_type} {identifier};")
        self.main_instances.append(f"assign {identifier} = {expr_value};")

    def visit_if(self, node):
        condition = self.visit_expression(node.children[0])[1]
        then_block = self.visit_block(node.children[1])
        else_block = self.visit_block(node.children[2]) if len(node.children) > 2 else None
        code = f"always @(*) begin\n    if ({condition}) begin\n{then_block}    end"
        if else_block:
            code += f"\n    else begin\n{else_block}    end"
        code += "\nend"
        self.main_instances.append(code)

    def visit_for(self, node):
        loop_var = node.children[0].value
        limit = self.visit_expression(node.children[1])[1]
        body = self.visit_block(node.children[2])
        self.variables[loop_var] = "wire [31:0]"
        code = f"for (int {loop_var} = 0; {loop_var} < {limit}; {loop_var} = {loop_var} + 1) begin\n{body}end"
        self.main_instances.append(code)

    def visit_while(self, node):
        condition = self.visit_expression(node.children[0])[1]
        body = self.visit_block(node.children[1])
        code = f"while ({condition}) begin\n{body}end"
        self.main_instances.append(code)

    def visit_function(self, node):
        func_name = node.value
        params = node.children[0].children
        body = node.children[1]
        param_decls = []
        for param in params:
            param_name = param.value
            self.variables[param_name] = "wire [31:0]"
            param_decls.append(f"input wire [31:0] {param_name}")
        param_str = ", ".join(param_decls)
        body_code = self.visit_block(body)
        code = f"function void {func_name}({param_str});\n{body_code}endfunction"
        self.main_instances.append(code)

    def visit_print(self, node):
        expr_type, expr_value = self.visit_expression(node.children[0])
        if expr_type == "string":
            expr_value = expr_value.replace('"', '\\"')  # Escapa as aspas
            self.display_statements.append(f'$display("{expr_value}");')
        else:
            self.display_statements.append(f'$display("%0d", {expr_value});')

    def visit_block(self, node):
        code = []
        for child in node.children:
            self.visit(child)
        return "\n".join(code)

    def visit_expression(self, node):
        if node.type == 'number':
            if isinstance(node.value, int):
                return ('int', str(node.value))
            elif isinstance(node.value, float):
                return ('real', str(node.value))
        elif node.type == 'string':
            return ('string', node.value)
        elif node.type == 'bool':
            return ('wire', "1" if node.value else "0")
        elif node.type == 'identifier':
            if node.value not in self.variables:
                raise ValueError(f"Erro: Variável '{node.value}' não declarada.")
            return (self.variables[node.value], node.value)
        elif node.type == 'operation':
            left_type, left = self.visit_expression(node.children[0])
            right_type, right = self.visit_expression(node.children[1])
            expr_type = "real" if "real" in (left_type, right_type) else "int"
            return (expr_type, f"({left} {node.operator} {right})")
        elif node.type == 'logical':
            left_type, left = self.visit_expression(node.children[0])
            right_type, right = self.visit_expression(node.children[1])
            op = "&&" if node.operator == "and" else "||"
            return ("wire", f"({left} {op} {right})")
        elif node.type == 'bitwise':
            left_type, left = self.visit_expression(node.children[0])
            right_type, right = self.visit_expression(node.children[1])
            expr_type = "real" if "real" in (left_type, right_type) else "int"
            return (expr_type, f"({left} {node.operator} {right})")
        elif node.type == 'comparison':
            left_type, left = self.visit_expression(node.children[0])
            right_type, right = self.visit_expression(node.children[1])
            return ("wire", f"({left} {node.operator} {right})")
        elif node.type == 'unary':
            operand_type, operand = self.visit_expression(node.children[0])
            if node.operator == "not":
                return ("wire", f"(!{operand})")
            return (operand_type, f"({node.operator}{operand})")
        raise ValueError(f"Erro: '{node.type}' não é permitido.")

def generate_systemverilog(ast):
    generator = SystemVerilogGenerator()
    return generator.generate(ast)