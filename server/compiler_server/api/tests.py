from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class CompilerAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_compile_basic_arithmetic(self):
        """Testa a compilação de uma atribuição simples e chamada de print."""
        # Código Python de entrada
        input_code = "x = 1 + 2\nprint(x)"

        # Faz a requisição POST para a rota /api/compile/
        response = self.client.post(
            '/api/compile/',
            {'code': input_code},
            format='json'
        )

        # Verifica se a resposta tem status 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Extrai os dados da resposta
        data = response.json()

        # Verifica se as chaves esperadas estão presentes
        self.assertIn('tokens', data)
        self.assertIn('ast', data)
        self.assertIn('systemverilog', data)

        # Verifica os tokens gerados (exemplo básico)
        expected_tokens = [
            ['ID', 'x'], ['ASSIGN', '='], ['NUMBER', '1'], ['PLUS', '+'], 
            ['NUMBER', '2'], ['NEWLINE', '\n'], ['ID', 'print'], ['LPAREN', '('], 
            ['ID', 'x'], ['RPAREN', ')'], ['NEWLINE', '\n']
        ]
        self.assertEqual(data['tokens'], expected_tokens)

        # Verifica a AST (como string, já que a estrutura exata pode variar um pouco)
        expected_ast_substring = "program[assignment[identifier(x), binary_op(+)[number(1), number(2)]], function_call(print)[identifier(x)]]"
        self.assertEqual(data['ast'], expected_ast_substring)

        # Verifica partes do SystemVerilog gerado
        sv_code = data['systemverilog']
        self.assertIn("module assign_x", sv_code)
        self.assertIn("assign x = (1 + 2);", sv_code)
        self.assertIn("module print_x", sv_code)
        self.assertIn("$display(x);", sv_code)
        self.assertIn("module main;", sv_code)
        self.assertIn("assign_x_inst", sv_code)
        self.assertIn("print_x_inst", sv_code)
