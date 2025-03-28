from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class Etapa1TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_print_number_systemverilog(self):
        """Testa a geração de SystemVerilog para um print simples com número."""
        input_code = "print(12)"
        response = self.client.post('/api/compile/', {'code': input_code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        sv_code = data['systemverilog']
        expected_sv_code = (
            "module main;\n"
            "    initial begin\n"
            "        $display(\"%0d\", 12);\n"
            "    end\n"
            "endmodule"
        )
        self.assertEqual(sv_code, expected_sv_code, "Código SystemVerilog gerado não corresponde ao esperado.")

    def test_print_string_systemverilog(self):
        """Testa a geração de SystemVerilog para um print com string."""
        input_code = 'print("Hello, World!")'
        response = self.client.post('/api/compile/', {'code': input_code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        sv_code = data['systemverilog']
        expected_sv_code = (
            "module main;\n"
            "    initial begin\n"
            "        $display(\"\\\"Hello, World!\\\"\");\n"
            "    end\n"
            "endmodule"
        )
        self.assertEqual(sv_code, expected_sv_code, "Código SystemVerilog gerado não corresponde ao esperado.")

    def test_simple_assignment_systemverilog(self):
        """Testa a geração de SystemVerilog para uma atribuição simples."""
        input_code = "x = 42"
        response = self.client.post('/api/compile/', {'code': input_code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        sv_code = data['systemverilog']
        expected_sv_code = (
            "module main;\n"
            "    int x;\n"
            "    assign x = 42;\n"
            "endmodule"
        )
        self.assertEqual(sv_code, expected_sv_code, "Código SystemVerilog gerado não corresponde ao esperado.")

    def test_float_assignment_systemverilog(self):
        """Testa a geração de SystemVerilog para uma atribuição com float."""
        input_code = "y = 3.14"
        response = self.client.post('/api/compile/', {'code': input_code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        sv_code = data['systemverilog']
        expected_sv_code = (
            "module main;\n"
            "    real y;\n"
            "    assign y = 3.14;\n"
            "endmodule"
        )
        self.assertEqual(sv_code, expected_sv_code, "Código SystemVerilog gerado não corresponde ao esperado.")

    def test_boolean_assignment_systemverilog(self):
        """Testa a geração de SystemVerilog para uma atribuição com booleano."""
        input_code = "z = True"
        response = self.client.post('/api/compile/', {'code': input_code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        sv_code = data['systemverilog']
        expected_sv_code = (
            "module main;\n"
            "    wire z;\n"
            "    assign z = 1;\n"
            "endmodule"
        )
        self.assertEqual(sv_code, expected_sv_code, "Código SystemVerilog gerado não corresponde ao esperado.")

    def test_if_statement_systemverilog(self):
        """Testa a geração de SystemVerilog para uma estrutura if simples."""
        input_code = (
            "x = 10\n"
            "if x > 5:\n"
            "    y = 20\n"
        )
        response = self.client.post('/api/compile/', {'code': input_code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        sv_code = data['systemverilog']
        expected_sv_code = (
            "module main;\n"
            "    int x;\n"
            "    int y;\n"
            "    assign x = 10;\n"
            "    always @(*) begin\n"
            "        if (x > 5) begin\n"
            "            assign y = 20;\n"
            "        end\n"
            "    end\n"
            "endmodule"
        )
        self.assertEqual(sv_code, expected_sv_code, "Código SystemVerilog gerado não corresponde ao esperado.")

    def test_for_loop_systemverilog(self):
        """Testa a geração de SystemVerilog para um loop for simples."""
        input_code = (
            "for i in 5:\n"
            "    x = i + 1\n"
        )
        response = self.client.post('/api/compile/', {'code': input_code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        sv_code = data['systemverilog']
        expected_sv_code = (
            "module main;\n"
            "    int i;\n"
            "    int x;\n"
            "    for (int i = 0; i < 5; i = i + 1) begin\n"
            "            assign x = (i + 1);\n"
            "    end\n"
            "endmodule"
        )
        self.assertEqual(sv_code, expected_sv_code, "Código SystemVerilog gerado não corresponde ao esperado.")

    def test_while_loop_systemverilog(self):
        """Testa a geração de SystemVerilog para um loop while simples."""
        input_code = (
            "x = 0\n"
            "while x < 3:\n"
            "    x = x + 1\n"
        )
        response = self.client.post('/api/compile/', {'code': input_code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        sv_code = data['systemverilog']
        expected_sv_code = (
            "module main;\n"
            "    int x;\n"
            "    assign x = 0;\n"
            "    while (x < 3) begin\n"
            "            assign x = (x + 1);\n"
            "    end\n"
            "endmodule"
        )
        self.assertEqual(sv_code, expected_sv_code, "Código SystemVerilog gerado não corresponde ao esperado.")

    def test_complex_flow_1_systemverilog(self):
        """Testa um fluxo complexo com if aninhado, for e print."""
        input_code = (
            "x = 0\n"
            "for i in 10:\n"
            "    if i > 5:\n"
            "        x = x + i\n"
            "        if x > 20:\n"
            "            print(x)\n"
            "    else:\n"
            "        x = x + 1\n"
        )
        response = self.client.post('/api/compile/', {'code': input_code}, format='json')
        if response.status_code != status.HTTP_200_OK:
            print("Erro retornado:", response.json())  # Adiciona print para depuração
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        sv_code = data['systemverilog']
        expected_sv_code = (
            "module main;\n"
            "    int x;\n"
            "    int i;\n"
            "    assign x = 0;\n"
            "    for (int i = 0; i < 10; i = i + 1) begin\n"
            "            always @(*) begin\n"
            "                if (i > 5) begin\n"
            "                    assign x = (x + i);\n"
            "                    always @(*) begin\n"
            "                        if (x > 20) begin\n"
            "                        end\n"
            "                    end\n"
            "                end\n"
            "                else begin\n"
            "                    assign x = (x + 1);\n"
            "                end\n"
            "            end\n"
            "    end\n"
            "    initial begin\n"
            "        $display(\"%0d\", x);\n"
            "    end\n"
            "endmodule"
        )
        self.assertEqual(sv_code, expected_sv_code, "Código SystemVerilog gerado não corresponde ao esperado.")

    def test_complex_flow_2_systemverilog(self):
        """Testa um fluxo complexo com função, while, if e print."""
        input_code = (
            "def sum(a, b):\n"
            "    result = a + b\n"
            "    return result\n"
            "x = 0\n"
            "while x < 100:\n"
            "    if x < 50:\n"
            "        x = sum(x, 10)\n"
            "        print(x)\n"
            "    else:\n"
            "        x = sum(x, 5)\n"
            "        print(x)\n"
        )
        response = self.client.post('/api/compile/', {'code': input_code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        sv_code = data['systemverilog']
        expected_sv_code = (
            "module main;\n"
            "    int result;\n"
            "    int a;\n"
            "    int b;\n"
            "    int x;\n"
            "    function void sum(input int a, input int b);\n"
            "            assign result = (a + b);\n"
            "    endfunction\n"
            "    assign x = 0;\n"
            "    while (x < 100) begin\n"
            "            always @(*) begin\n"
            "                if (x < 50) begin\n"
            "                    sum(x, 10);\n"
            "                    assign x = result;\n"
            "                end\n"
            "                else begin\n"
            "                    sum(x, 5);\n"
            "                    assign x = result;\n"
            "                end\n"
            "            end\n"
            "    end\n"
            "    initial begin\n"
            "        $display(\"%0d\", x);\n"
            "        $display(\"%0d\", x);\n"
            "    end\n"
            "endmodule"
        )
        self.assertEqual(sv_code, expected_sv_code, "Código SystemVerilog gerado não corresponde ao esperado.")