http://127.0.0.1:8000/api/hello/

cd server

cd compiler_server

python manage.py runserver

python manage.py test api


# Manual Detalhado das Operações Permitidas

Aqui está o manual que detalha o que o Python pode fazer e o que o SystemVerilog aceitará através do nosso compilador. Ele serve como um guia para os usuários e define os limites do subconjunto suportado.

## Manual de Operações Permitidas em Python para Tradução em SystemVerilog

Este manual descreve as construções e operações em Python que nosso compilador aceita para tradução em SystemVerilog. Qualquer código fora deste subconjunto pode gerar erros ou não ser traduzido corretamente.

---

## 1. Variáveis e Tipos de Dados

### **Tipos Suportados:**
- `int`: Inteiros (ex.: `x = 5`).
- `float`: Números de ponto flutuante (ex.: `y = 3.14`).
- `bool`: Valores booleanos (`True`, `False`).
- `str`: Strings simples (ex.: `nome = "teste"`), sem operações avançadas como `.format()`.

### **Regras:**
- Variáveis devem ser declaradas antes do uso.
- O tipo de uma variável não pode mudar (sem tipagem dinâmica).

---

## 2. Operações

### **Operações Suportadas:**
- **Aritméticas:** `+`, `-`, `*`, `/`, `%`.
- **Lógicas:** `and`, `or`, `not`.
- **De Bits:** `&` (AND), `|` (OR), `^` (XOR), `~` (NOT), `<<` (shift esquerdo), `>>` (shift direito).
- **Comparações:** `==`, `!=`, `<`, `>`, `<=`, `>=`.

### **Exemplo:**
```python
x = 5 + 3
y = x & 2
z = x > 0
```

---

## 3. Controle de Fluxo

### **If-Else:**
- Suporta condições simples e aninhadas.

#### **Exemplo:**
```python
if x > 0:
    y = 1
else:
    y = 0
```

### **For Loops:**
- Apenas loops com limites fixos definidos em tempo de compilação.

#### **Exemplo:**
```python
for i in range(10):
    print(i)
```

### **While Loops:**
- Condições simples que garantam terminação.

#### **Exemplo:**
```python
while x < 5:
    x += 1
```

---

## 4. Funções

### **Definição:**
- Funções sem recursão, com argumentos e retornos dos tipos suportados.

#### **Exemplo:**
```python
def soma(a, b):
    return a + b

z = soma(2, 3)
```

---

## 5. Restrições

- **Sem Tipagem Dinâmica:** Uma variável não pode mudar de tipo (ex.: de `int` para `str`).
- **Sem Estruturas Complexas:** Nada de dicionários, conjuntos ou listas heterogêneas.
- **Sem Exceções:** Não use `try-except`.
- **Sem Operações de I/O:** Exceto `print` para depuração.
