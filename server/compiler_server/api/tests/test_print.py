from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import re

class SyslogPyCompilerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_hello_world_module(self):
        """Testa a geração de Python a partir de um Verilog simples com $display."""
        input_code = (
            "module test;\n"
            "  initial\n"
            "    begin\n"
            "      $display(\"Hello, World!\");\n"
            "    end\n"
            "endmodule"
        )
        response = self.client.post('/api/compile-syslog-py/', {'code': input_code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Erro na API: {response.json()}")

        data = response.json()
        py_code = data['python']

        # Padrão regex para o código esperado, com ID dinâmico
        expected_pattern = (
            r"from sys import argv\n"
            r"# Module: test \(ID: [a-f0-9]{8}\)\n"
            r"# Initial block\n"
            r"print\(\"Hello, World!\"\)\n"
            r"# End of module: test"
        )

        self.assertTrue(
            re.fullmatch(expected_pattern, py_code.strip()),
            f"Código Python gerado não corresponde ao esperado.\n"
            f"Padrão esperado: {expected_pattern}\n"
            f"Gerado: {py_code}"
        )

    def test_empty_module(self):
        """Testa um módulo vazio para garantir que o compilador não falha."""
        input_code = (
            "module empty;\n"
            "endmodule"
        )
        response = self.client.post('/api/compile-syslog-py/', {'code': input_code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Erro na API: {response.json()}")

        data = response.json()
        py_code = data['python']

        # Padrão regex para o código esperado, com ID dinâmico
        expected_pattern = (
            r"from sys import argv\n"
            r"# Module: empty \(ID: [a-f0-9]{8}\)\n"
            r"# End of module: empty"
        )

        self.assertTrue(
            re.fullmatch(expected_pattern, py_code.strip()),
            f"Código Python gerado não corresponde ao esperado.\n"
            f"Padrão esperado: {expected_pattern}\n"
            f"Gerado: {py_code}"
        )