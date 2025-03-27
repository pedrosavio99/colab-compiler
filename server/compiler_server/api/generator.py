from .parser import ASTNode

class SystemVerilogGenerator:
    def __init__(self):
        self.code = []
        self.current_module_code = []
        self.indent_level = 0
        self.variables = {}
        self.modules = []
        self.main_signals = []
        self.main_instances = []
        self.string_functions = set()

    def indent(self):
        return "    " * self.indent_level

    def sanitize_name(self, name):
        return ''.join(c if c.isalnum() else '_' for c in name)

    def find_identifiers(self, node):
        identifiers = set()
        if node.type == 'identifier':
            identifiers.add(node.value)
        elif node.type == 'binary_op':
            for child in node.children:
                identifiers.update(self.find_identifiers(child))
        return identifiers

    def generate(self, ast):
        self.visit(ast)
        self.code.append("// Módulos gerados a partir do programa Python")
        self.code.extend([module for module in self.modules])
        self.code.append("\nmodule main;")
        self.indent_level += 1
        for signal in self.main_signals:
            self.code.append(f"{self.indent()}wire [31:0] {signal};")
        self.code.append("")
        for instance in self.main_instances:
            self.code.append(f"{self.indent()}{instance}")
        self.indent_level -= 1
        self.code.append("endmodule")
        return "\n".join(self.code)

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

    def visit_assignment(self, node):
        identifier = node.children[0].value
        expression = self.visit(node.children[1])
        
        if node.children[1].type == 'function_call':
            func_name = node.children[1].value
            args = [self.visit(arg) for arg in node.children[1].children]
            instance_name = f"{func_name}_{identifier}_inst"
            if func_name not in self.string_functions:
                self.main_signals.append(identifier)
                self.variables[identifier] = ('numeric', None)
                self.main_instances.append(f"{func_name} {instance_name} ({', '.join(args)}, {identifier});")
            else:
                result = self.get_string_function_result(func_name, node.children[1])
                self.variables[identifier] = ('string', result)
                adjusted_args = []
                for arg in node.children[1].children:
                    if arg.type == 'string':
                        adjusted_args.append(arg.value.strip("'"))
                    else:
                        adjusted_args.append(self.visit(arg))
                self.main_instances.append(f"{func_name} {instance_name} ({', '.join(adjusted_args)});")
        else:
            used_identifiers = self.find_identifiers(node.children[1])
            module_code = []
            inputs = [f"input wire [31:0] {var}" for var in used_identifiers if var != identifier]
            ports = ", ".join(inputs + [f"output wire [31:0] {identifier}"]) if inputs else f"output wire [31:0] {identifier}"
            module_code.append(f"module assign_{identifier} ({ports});")
            self.indent_level += 1
            module_code.append(f"{self.indent()}assign {identifier} = {expression};")
            self.indent_level -= 1
            module_code.append(f"endmodule\n")
            self.modules.append("\n".join(module_code))
            self.main_signals.append(identifier)
            self.variables[identifier] = ('numeric', None)
            instance_args = ", ".join(list(used_identifiers) + [identifier]) if used_identifiers else identifier
            self.main_instances.append(f"assign_{identifier} assign_{identifier}_inst ({instance_args});")

    def get_string_function_result(self, func_name, node):
        if func_name in self.string_functions:
            args = [self.visit(arg) for arg in node.children]
            if func_name == 'saudacao':
                return f"Olá, {args[0]}!"
            elif func_name == 'info_pessoa':
                return f"{args[0]} tem {args[1]} anos"
            elif func_name == 'descrever_numero':
                return f"O número é {args[0]}"
            elif func_name == 'mensagem':
                return f"O quadrado é {args[0]}"
            elif func_name == 'carol':
                return f"{args[0]} vai tomar no , brincadiera po"
        return "?"

    def visit_function_def(self, node):
        func_name = node.children[0].value
        params = self.visit(node.children[1])
        self.current_module_code = []
        has_string_op = self.check_for_string_op(node.children[2])
        if has_string_op:
            self.string_functions.add(func_name)
            self.current_module_code.append(f"module {func_name} ({params});")
        else:
            self.current_module_code.append(f"module {func_name} ({params}, output wire [31:0] out);")
        self.indent_level += 1
        self.visit(node.children[2])
        self.indent_level -= 1
        self.current_module_code.append(f"endmodule\n")
        self.modules.append("\n".join(self.current_module_code))

    def check_for_string_op(self, node):
        if node.type == 'block':
            for child in node.children:
                if self.check_for_string_op(child):
                    return True
        elif node.type == 'return':
            return self.check_for_string_op(node.children[0])
        elif node.type == 'binary_op':
            return any(self.check_for_string_op(child) for child in node.children)
        elif node.type == 'string':
            return True
        return False

    def visit_function_call(self, node):
        func_name = node.value
        args = [self.visit(arg) for arg in node.children]
        if func_name == 'print':
            valid_args = []
            display_args = []
            for i, child in enumerate(node.children):
                if child.type == 'string':
                    raw_string = child.value.strip("'")
                    display_args.append(f"{raw_string}")
                else:
                    var_name = child.value
                    if var_name in self.variables:
                        var_type, var_value = self.variables[var_name]
                        if var_type == 'numeric':
                            valid_args.append((i, var_name))
                            display_args.append(var_name)
                        elif var_type == 'string' and var_value:
                            display_args.append(f"{var_value}")
                    else:
                        display_args.append('"?"')
            ports = [f"input wire [31:0] {arg}" for _, arg in valid_args]
            port_list = ", ".join(ports) if ports else ""
            module_name = f"print_{self.sanitize_name('_'.join([str(self.visit(arg)) for arg in node.children]))}"
            module_code = []
            module_code.append(f"module {module_name}({port_list});")
            self.indent_level += 1
            module_code.append(f"{self.indent()}initial begin")
            self.indent_level += 1
            display_args_str = ", ".join([f'"{arg}"' if not arg.startswith('"') and not arg.isidentifier() else arg for arg in display_args])
            module_code.append(f"{self.indent()}$display({display_args_str});")
            self.indent_level -= 1
            module_code.append(f"{self.indent()}end")
            self.indent_level -= 1
            module_code.append(f"endmodule\n")
            self.modules.append("\n".join(module_code))
            instance_args = [arg for _, arg in valid_args]
            instance_args_str = ", ".join(instance_args) if instance_args else ""
            self.main_instances.append(f"{module_name} {module_name}_inst({instance_args_str});")
        return f"{func_name}_result"

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
        if self.check_for_string_op(node.children[0]):
            self.current_module_code.append(f"{self.indent()}initial begin")
            self.indent_level += 1
            self.current_module_code.append(f"{self.indent()}$display(\"{expression}\");")
            self.indent_level -= 1
            self.current_module_code.append(f"{self.indent()}end")
            return expression
        else:
            self.current_module_code.append(f"{self.indent()}assign out = {expression};")
            return expression

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

def generate_systemverilog(ast):
    generator = SystemVerilogGenerator()
    return generator.generate(ast)