from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class ConcatMonitorTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_concat_with_monitor(self):
        """Testa a geração de Python a partir de um Verilog com concatenação e $monitor."""
        input_code = (
            "module main (\n"
            "    input logic a,\n"
            "    input logic b,\n"
            "    input logic clk,\n"
            "    output logic [1:0] y\n"
            ");\n"
            "    reg [1:0] temp;\n"
            "    always @(posedge clk) begin\n"
            "        temp <= {a, b};\n"
            "        y <= temp;\n"
            "    end\n"
            "    initial begin\n"
            "        $monitor(\"Tempo: %t | a: %b | b: %b | y: %b\", $time, a, b, y);\n"
            "        #50 $finish;\n"
            "    end\n"
            "endmodule"
        )
        response = self.client.post('/api/compile-syslog-py/', {'code': input_code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Erro na API: {response.json()}")

        # Extrai apenas o 'python' do payload
        data = response.json()
        py_code = data['python']

        # Código Python esperado
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
            "\n"
            "class main:\n"
            "    def __init__(self):\n"
            "        self.a = Signal(bit_width=None)  # input, logic\n"
            "        self.b = Signal(bit_width=None)  # input, logic\n"
            "        self.clk = Signal(bit_width=None)  # input, logic\n"
            "        self.y = Signal(bit_width=(1, 0))  # output, logic, [1:0]\n"
            "        self.temp = Signal(bit_width=(1, 0))  # reg\n"
            "        self.time = 0  # Simulação de $time\n"
            "\n"
            "    def update_combinational(self):\n"
            "        pass\n"
            "\n"
            "    def update_sequential(self):\n"
            "        # Sensível a posedge de clk\n"
            "        # Simulação simplificada: atualiza na borda\n"
            "        self.temp.set_value((self.b.value << 0) | (self.a.value << 1))\n"
            "        self.y.set_value(self.temp.value)\n"
            "\n"
            "    def run_initial(self):\n"
            "        # Simulação do bloco initial\n"
            "        print(f\"Tempo: {self.time} | a: {self.a.value:b} | b: {self.b.value:b} | y: {self.y.value:b}\")\n"
            "        if self.time == 50:\n"
            "            return False  # $finish\n"
            "        return True\n"
            "\n"
            "    def run(self):\n"
            "        while self.run_initial():\n"
            "            self.update_combinational()\n"
            "            self.update_sequential()\n"
            "            self.time += 1  # Default time step\n"
            "\n"
            "# Teste manual\n"
            "if __name__ == \"__main__\":\n"
            "    sim = main()\n"
            "    sim.run()"
        )

        # Compara apenas o código Python
        self.assertEqual(py_code.strip(), expected_py_code.strip(), "Código Python gerado não corresponde ao esperado.")