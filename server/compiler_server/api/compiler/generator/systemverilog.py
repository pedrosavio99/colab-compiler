from ..parser.ast import ASTNode

class SystemVerilogGenerator:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.current_scope = []
        self.display_statements = []  # Para armazenar os $display e agrupá-los no bloco initial

    def generate(self, ast):
        if ast is None:
            return ""
        if ast.type == 'program':
            code = ["module main;"]
            for statement in ast.children:
                gen_code = self.generate(statement)
                if gen_code and not statement.type == 'print':  # $display será tratado separadamente
                    code.append(gen_code)
            # Adiciona as declarações de variáveis
            for var, var_type in self.variables.items():
                code.append(f"    {var_type} {var};")
            # Adiciona as instâncias (como assign)
            for statement in ast.children:
                if statement.type == 'assignment':
                    identifier = statement.children[0].value
                    expr_code = self.generate_expression(statement.children[1])
                    code.append(f"    assign {identifier} = {expr_code};")
            # Adiciona o bloco initial com os $display
            if self.display_statements:
                code.append("    initial begin")
                code.extend([f"        {stmt}" for stmt in self.display_statements])
                code.append("    end")
            code.append("endmodule")
            return "\n".join(code)
        elif ast.type == 'assignment':
            identifier = ast.children[0].value
            expression = ast.children[1]
            var_type = self.determine_type(expression)
            if identifier in self.variables:
                if self.variables[identifier] != var_type:
                    raise ValueError(f"Erro: Tipagem dinâmica não permitida. '{identifier}' já foi definido como {self.variables[identifier]}.")
            else:
                self.variables[identifier] = var_type
            return ""  # Não retorna código aqui, será tratado no nível do programa
        elif ast.type == 'if':
            condition = self.generate_expression(ast.children[0])
            then_block = self.generate_block(ast.children[1])
            else_block = self.generate_block(ast.children[2]) if len(ast.children) > 2 else None
            code = f"    always @(*) begin\n        if ({condition}) begin\n{then_block}        end"
            if else_block:
                code += f"\n        else begin\n{else_block}        end"
            code += "\n    end"
            return code
        elif ast.type == 'for':
            loop_var = ast.children[0].value
            limit = self.generate_expression(ast.children[1])
            body = self.generate_block(ast.children[2])
            self.variables[loop_var] = "wire [31:0]"
            code = f"    for (int {loop_var} = 0; {loop_var} < {limit}; {loop_var} = {loop_var} + 1) begin\n{body}    end"
            return code
        elif ast.type == 'while':
            condition = self.generate_expression(ast.children[0])
            body = self.generate_block(ast.children[1])
            code = f"    while ({condition}) begin\n{body}    end"
            return code
        elif ast.type == 'function':
            func_name = ast.value
            params = ast.children[0].children
            body = ast.children[1]
            param_decls = []
            for param in params:
                param_name = param.value
                self.variables[param_name] = "wire [31:0]"
                param_decls.append(f"input wire [31:0] {param_name}")
            param_str = ", ".join(param_decls)
            self.functions[func_name] = [p.value for p in params]
            body_code = self.generate_block(body)
            code = f"    function void {func_name}({param_str});\n{body_code}    endfunction"
            return code
        elif ast.type == 'print':
            expr = self.generate_expression(ast.children[0])
            expr_type = self.determine_type(ast.children[0])
            if expr_type == "string":
                self.display_statements.append(f'$display("{expr}");')
            else:
                self.display_statements.append(f'$display("%0d", {expr});')
            return ""  # Não retorna código aqui, será tratado no bloco initial
        return ""

    def generate_block(self, node):
        if node.type != 'block':
            return self.generate(node)
        code = []
        for stmt in node.children:
            stmt_code = self.generate(stmt)
            if stmt_code:
                code.append(f"            {stmt_code}")
        return "\n".join(code)

    def generate_expression(self, node):
        if node.type == 'number':
            return str(node.value)
        elif node.type == 'string':
            return node.value
        elif node.type == 'bool':
            return "1" if node.value else "0"
        elif node.type == 'identifier':
            if node.value not in self.variables:
                raise ValueError(f"Erro: Variável '{node.value}' não declarada.")
            return node.value
        elif node.type == 'operation':
            left = self.generate_expression(node.children[0])
            right = self.generate_expression(node.children[1])
            return f"({left} {node.operator} {right})"
        elif node.type == 'logical':
            left = self.generate_expression(node.children[0])
            right = self.generate_expression(node.children[1])
            op = "&&" if node.operator == "and" else "||"
            return f"({left} {op} {right})"
        elif node.type == 'bitwise':
            left = self.generate_expression(node.children[0])
            right = self.generate_expression(node.children[1])
            return f"({left} {node.operator} {right})"
        elif node.type == 'comparison':
            left = self.generate_expression(node.children[0])
            right = self.generate_expression(node.children[1])
            return f"({left} {node.operator} {right})"
        elif node.type == 'unary':
            operand = self.generate_expression(node.children[0])
            if node.operator == "not":
                return f"(!{operand})"
            return f"({node.operator}{operand})"
        raise ValueError(f"Tipo de nó '{node.type}' não suportado para geração de SystemVerilog.")

    def determine_type(self, node):
        if node.type == 'number':
            return "real" if isinstance(node.value, float) else "int"
        elif node.type == 'string':
            return "string"
        elif node.type == 'bool':
            return "wire"  # Alterado de "bit" para "wire"
        elif node.type == 'identifier':
            if node.value not in self.variables:
                raise ValueError(f"Erro: Variável '{node.value}' não declarada.")
            return self.variables[node.value]
        elif node.type in ('operation', 'bitwise', 'comparison'):
            left_type = self.determine_type(node.children[0])
            right_type = self.determine_type(node.children[1])
            if left_type == "real" or right_type == "real":
                return "real"
            return "int"
        elif node.type == 'logical':
            return "wire"  # Alterado de "bit" para "wire"
        elif node.type == 'unary':
            if node.operator == "not":
                return "wire"  # Alterado de "bit" para "wire"
            return self.determine_type(node.children[0])
        raise ValueError(f"Tipo de nó '{node.type}' não suportado para determinação de tipo.")