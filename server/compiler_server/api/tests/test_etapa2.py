from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class SyslogPyTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_counter_with_monitor(self):
        """Testa a geração de Python a partir de um Verilog com contador, clock e $monitor."""
        input_code = (
            "module main;\n"
            "  reg clk = 0;\n"
            "  reg reset = 1;\n"
            "  reg [1:0] count;\n"
            "  always #5 clk = ~clk;\n"
            "  always @(posedge clk or posedge reset) begin\n"
            "    if (reset)\n"
            "      count <= 2'b00;\n"
            "    else if (count == 2'b11)\n"
            "      count <= 2'b00;\n"
            "    else\n"
            "      count <= count + 1;\n"
            "  end\n"
            "  initial begin\n"
            "    $monitor(\"Tempo: %t | Count: %d\", $time, count);\n"
            "    #10 reset = 0;\n"
            "    #60 $finish;\n"
            "  end\n"
            "endmodule"
        )
        response = self.client.post('/api/compile-syslog-py/', {'code': input_code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Erro na API: {response.json()}")
        data = response.json()
        py_code = data['python']
        
        expected_py_code = (
            "class Signal:\n"
            "    def __init__(self, value=0, bit_width=None):\n"
            "        self.value = value\n"
            "        self.bit_width = bit_width\n"
            "        if bit_width:\n"
            "            self.max_value = (1 << (bit_width[0] - bit_width[1] + 1)) - 1\n"
            "\n"
            "    def set_value(self, value):\n"
            "        if self.bit_width:\n"
            "            self.value = value & self.max_value\n"
            "        else:\n"
            "            self.value = value\n"
            "\n"
            "class main:\n"
            "    def __init__(self):\n"
            "        self.clk = Signal(bit_width=None, value=0)  # reg\n"
            "        self.reset = Signal(bit_width=None, value=1)  # reg\n"
            "        self.count = Signal(bit_width=(1, 0))  # reg\n"
            "        self.time = 0  # Simulação de $time\n"
            "\n"
            "    def update_combinational(self):\n"
            "        pass\n"
            "\n"
            "    def update_sequential(self):\n"
            "        # Clock gerado com atraso de 5 unidades\n"
            "        # Simulação simplificada: alterna o sinal\n"
            "        self.clk.set_value(~ self.clk.value)\n"
            "        # Sensível a posedge de clk, posedge de reset\n"
            "        # Simulação simplificada: atualiza na borda\n"
            "        if self.reset.value:\n"
            "            self.count.set_value(0)\n"
            "        else:\n"
            "            if self.count.value == 3:\n"
            "                self.count.set_value(0)\n"
            "            else:\n"
            "                self.count.set_value(self.count.value + 1)\n"
            "\n"
            "    def run_initial(self):\n"
            "        # Simulação do bloco initial\n"
            "        print(f\"Tempo: {self.time} | Count: {self.count.value}\")\n"
            "        if self.time == 10:\n"
            "            self.reset.set_value(0)\n"
            "        if self.time == 60:\n"
            "            return False  # $finish\n"
            "        return True\n"
            "\n"
            "    def run(self):\n"
            "        while self.run_initial():\n"
            "            self.update_combinational()\n"
            "            self.update_sequential()\n"
            "            self.time += 5\n"
            "\n"
            "# Teste manual\n"
            "if __name__ == \"__main__\":\n"
            "    sim = main()\n"
            "    sim.run()"
        )
        self.assertEqual(py_code.strip(), expected_py_code.strip(), "Código Python gerado não corresponde ao esperado.")

    def test_simple_clock(self):
        """Testa a geração de Python a partir de um Verilog simples com clock e $finish."""
        input_code = (
            "module main;\n"
            "  reg clk = 0;\n"
            "  always #5 clk = ~clk;\n"
            "  initial begin\n"
            "    #50 $finish;\n"
            "  end\n"
            "endmodule"
        )
        response = self.client.post('/api/compile-syslog-py/', {'code': input_code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Erro na API: {response.json()}")
        data = response.json()
        py_code = data['python']
        
        expected_py_code = (
            "class Signal:\n"
            "    def __init__(self, value=0, bit_width=None):\n"
            "        self.value = value\n"
            "        self.bit_width = bit_width\n"
            "        if bit_width:\n"
            "            self.max_value = (1 << (bit_width[0] - bit_width[1] + 1)) - 1\n"
            "\n"
            "    def set_value(self, value):\n"
            "        if self.bit_width:\n"
            "            self.value = value & self.max_value\n"
            "        else:\n"
            "            self.value = value\n"
            "\n"
            "class main:\n"
            "    def __init__(self):\n"
            "        self.clk = Signal(bit_width=None, value=0)  # reg\n"
            "        self.time = 0  # Simulação de $time\n"
            "\n"
            "    def update_combinational(self):\n"
            "        pass\n"
            "\n"
            "    def update_sequential(self):\n"
            "        # Clock gerado com atraso de 5 unidades\n"
            "        # Simulação simplificada: alterna o sinal\n"
            "        self.clk.set_value(~ self.clk.value)\n"
            "\n"
            "    def run_initial(self):\n"
            "        # Simulação do bloco initial\n"
            "        if self.time == 50:\n"
            "            return False  # $finish\n"
            "        return True\n"
            "\n"
            "    def run(self):\n"
            "        while self.run_initial():\n"
            "            self.update_combinational()\n"
            "            self.update_sequential()\n"
            "            self.time += 5\n"
            "\n"
            "# Teste manual\n"
            "if __name__ == \"__main__\":\n"
            "    sim = main()\n"
            "    sim.run()"
        )
        self.assertEqual(py_code.strip(), expected_py_code.strip(), "Código Python gerado não corresponde ao esperado.")
