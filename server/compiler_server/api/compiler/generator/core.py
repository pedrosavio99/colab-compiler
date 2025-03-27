from .systemverilog import SystemVerilogGenerator as SVGen
from .utils import check_for_string_op  # Importamos a função necessária

class SystemVerilogGenerator(SVGen):
    def visit(self, node):
        if node.type == 'program':
            self.visit_program(node)
        elif node.type == 'assignment':
            self.visit_assignment(node)
        elif node.type == 'function_def':
            self.visit_function_def(node)
        elif node.type == 'function_call':
            return self.visit_function_call(node)
        elif node.type == 'binary_op':
            return self.visit_binary_op(node)
        elif node.type == 'identifier':
            return self.visit_identifier(node)
        elif node.type == 'number':
            return self.visit_number(node)
        elif node.type == 'string':
            return self.visit_string(node)
        elif node.type == 'param_list':
            return self.visit_param_list(node)
        elif node.type == 'block':
            self.visit_block(node)
        elif node.type == 'return':
            return self.visit_return(node)

    def visit_program(self, node):
        for child in node.children:
            self.visit(child)

    def visit_binary_op(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        return f"({left} {node.value} {right})"

    def visit_identifier(self, node):
        return node.value

    def visit_number(self, node):
        return node.value

    def visit_string(self, node):
        return node.value.strip("'")

    def visit_param_list(self, node):
        params = []
        for child in node.children:
            self.variables[child.value] = ('numeric', None)
            params.append(f"input wire [31:0] {child.value}")
        return ", ".join(params)

    def visit_block(self, node):
        for child in node.children:
            self.visit(child)

    def visit_return(self, node):
        expression = self.visit(node.children[0])
        if check_for_string_op(node.children[0]):  # Agora reconhecida
            self.current_module_code.append(f"{self.indent()}initial begin")
            self.indent_level += 1
            self.current_module_code.append(f"{self.indent()}$display(\"{expression}\");")
            self.indent_level -= 1
            self.current_module_code.append(f"{self.indent()}end")
            return expression
        else:
            self.current_module_code.append(f"{self.indent()}assign out = {expression};")
            return expression

def generate_systemverilog(ast):
    generator = SystemVerilogGenerator()
    return generator.generate(ast)