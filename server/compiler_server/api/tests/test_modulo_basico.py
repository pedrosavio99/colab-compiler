from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import re

class SyslogPyCompilerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_modulo_basico(self):
        """Testa a geração de Python a partir do módulo modulo_basico com always e if/else."""
        input_code = (
            "module modulo_basico (\n"
            "    input logic clk,\n"
            "    input logic [3:0] in_data,\n"
            "    output logic [3:0] out_data\n"
            ");\n"
            "    always @(posedge clk) begin\n"
            "        if (in_data > 5) begin\n"
            "            out_data <= in_data + 1;\n"
            "            $display(\"[SV] Valor alto: %d\", out_data);\n"
            "        end else begin\n"
            "            out_data <= in_data - 1;\n"
            "            $display(\"[SV] Valor baixo: %d\", out_data);\n"
            "        end\n"
            "    end\n"
            "endmodule"
        )
        response = self.client.post('/api/compile-syslog-py/', {'code': input_code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Erro na API: {response.json()}")

        data = response.json()
        py_code = data['python']

        # Padrão regex corrigido, escapando os colchetes [SV]
        expected_pattern = (
            r"# Module: modulo_basico \(ID: [a-f0-9]{8}\)\n"
            r"from sys import argv\n"
            r"\n"
            r"class Signal:\n"
            r"    def __init__\(self, value=0, width=None\):\n"
            r"        self\.value = value\n"
            r"        self\.width = width\n"
            r"        self\.prev_value = value\n"
            r"    def set_value\(self, value\):\n"
            r"        if self\.width:\n"
            r"            self\.value = value & \(\(1 << self\.width\) - 1\)\n"
            r"        else:\n"
            r"            self\.value = value\n"
            r"\n"
            r"class modulo_basico:\n"
            r"    def __init__\(self\):\n"
            r"        self\.clk = Signal\(0, None\)  # input logic\n"
            r"        self\.in_data = Signal\(0, 4\)  # input logic\n"
            r"        self\.out_data = Signal\(0, 4\)  # output logic\n"
            r"\n"
            r"    def update_always\(self\):\n"
            r"        # Sensível a posedge clk\n"
            r"        if self\.clk\.value and not self\.clk\.prev_value:  # Borda positiva\n"
            r"            if self\.in_data\.value>5:\n"
            r"                self\.out_data\.set_value\(self\.in_data\.value \+ 1\)\n"
            r"                print\(\"\[SV\] Valor alto: %d\"\.format\(self\.out_data\.value\)\)\n"
            r"            else:\n"
            r"                self\.out_data\.set_value\(self\.in_data\.value - 1\)\n"
            r"                print\(\"\[SV\] Valor baixo: %d\"\.format\(self\.out_data\.value\)\)\n"
            r"        self\.clk\.prev_value = self\.clk\.value\n"
            r"\n"
            r"    def run\(self, clk_value, in_data_value\):\n"
            r"        self\.clk\.set_value\(clk_value\)\n"
            r"        self\.in_data\.set_value\(in_data_value\)\n"
            r"        self\.update_always\(\)\n"
            r"        return self\.out_data\.value\n"
            r"# End of module: modulo_basico"
        )

        self.assertTrue(
            re.fullmatch(expected_pattern, py_code.strip()),
            f"Código Python gerado não corresponde ao esperado.\n"
            f"Padrão esperado: {expected_pattern}\n"
            f"Gerado: {py_code}"
        )