import React, { useState } from "react";
import AceEditor from "react-ace";
import Button from "./components/Button";
import "./index.css";

// Importa os modos e temas do Ace
import "ace-builds/src-noconflict/mode-verilog";
import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/theme-monokai";

const App = () => {
  const [screen, setScreen] = useState("register"); // Tracks current screen
  const [user, setUser] = useState(null); // Mock user data
  const [verilogCode, setVerilogCode] = useState(""); // Código Verilog inserido
  const [compiledResult, setCompiledResult] = useState(""); // Resultado da compilação
  const [activeEditor, setActiveEditor] = useState("verilog"); // Verilog começa aberto
  const [message, setMessage] = useState(""); // Mensagem de feedback para botões

  // Mock register function
  const handleRegister = (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const name = formData.get("name");
    const email = formData.get("email");
    const password = formData.get("password");
    setUser({ name, email, password });
    setScreen("login");
  };

  // Mock login function
  const handleLogin = (e) => {
    e.preventDefault();
    setScreen("home");
  };

  // Função para enviar o código Verilog para a API
  const handleCompile = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/compile-syslog-py/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code: verilogCode }),
      });

      const data = await response.json();
      if (response.ok) {
        setCompiledResult(data.python || "Compilação bem-sucedida, mas sem código Python retornado.");
        setActiveEditor("python"); // Abre o Python após compilar
        setMessage("Compilação realizada com sucesso!");
      } else {
        setCompiledResult(`Erro: ${data.error || "Erro desconhecido na API."}`);
        setActiveEditor("python");
        setMessage("Erro ao compilar o código.");
      }
    } catch (error) {
      setCompiledResult(`Erro de conexão: ${error.message}`);
      setActiveEditor("python");
      setMessage("Erro de conexão com o servidor.");
    }
    setTimeout(() => setMessage(""), 3000); // Limpa a mensagem após 3 segundos
  };

  // Função para copiar código para a área de transferência
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(
      () => setMessage("Código copiado com sucesso!"),
      (err) => setMessage(`Erro ao copiar código: ${err}`)
    );
    setTimeout(() => setMessage(""), 3000);
  };

  // Função para colar código da área de transferência
  const pasteFromClipboard = async (setCode) => {
    try {
      const text = await navigator.clipboard.readText();
      setCode(text);
      setMessage("Código colado com sucesso!");
    } catch (err) {
      setMessage(`Erro ao colar código: ${err}`);
    }
    setTimeout(() => setMessage(""), 3000);
  };

  // Função para alternar o editor ativo
  const toggleEditor = (editor) => {
    setActiveEditor(activeEditor === editor ? null : editor);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#8bd162] via-[#d6d2d2] to-[#d86c6c] flex items-center justify-center p-4">
      {/* Register Screen */}
      {screen === "register" && (
        <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md transform transition-all duration-500 scale-100 hover:scale-105">
          <h1 className="text-3xl font-bold text-center text-gray-800 mb-6 animate-fade-in-down">
            Register
          </h1>
          <form onSubmit={handleRegister} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Name</label>
              <input
                type="text"
                name="name"
                className="mt-1 w-full p-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-all duration-300"
                placeholder="Your Name"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Email</label>
              <input
                type="email"
                name="email"
                className="mt-1 w-full p-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-all duration-300"
                placeholder="your.email@example.com"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Password</label>
              <input
                type="password"
                name="password"
                className="mt-1 w-full p-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-all duration-300"
                placeholder="••••••••"
                required
              />
            </div>
            <Button
              type="submit"
              variant="primario"
              status="default"
              className="w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700 transition-all duration-300 transform hover:scale-105"
            >
              Register
            </Button>
          </form>
          <p className="mt-4 text-center text-sm text-gray-600">
            Already have an account?{" "}
            <button
              onClick={() => setScreen("login")}
              className="text-indigo-600 hover:underline"
            >
              Log in
            </button>
          </p>
        </div>
      )}

      {/* Login Screen */}
      {screen === "login" && (
        <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md transform transition-all duration-500 scale-100 hover:scale-105">
          <h1 className="text-3xl font-bold text-center text-gray-800 mb-6 animate-fade-in-down">
            Login
          </h1>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Email</label>
              <input
                type="email"
                name="email"
                className="mt-1 w-full p-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-all duration-300"
                placeholder="your.email@example.com"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Password</label>
              <input
                type="password"
                name="password"
                className="mt-1 w-full p-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-all duration-300"
                placeholder="••••••••"
                required
              />
            </div>
            <Button
              type="submit"
              variant="primario"
              status="default"
              className="w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700 transition-all duration-300 transform hover:scale-105"
            >
              Login
            </Button>
          </form>
          <p className="mt-4 text-center text-sm text-gray-600">
            Don’t have an account?{" "}
            <button
              onClick={() => setScreen("register")}
              className="text-indigo-600 hover:underline"
            >
              Register
            </button>
          </p>
        </div>
      )}

      {/* Home Screen */}
      {screen === "home" && (
        <div className="bg-[#FBFBFE] rounded-2xl shadow-2xl p-8 w-full max-w-4xl transform transition-all duration-500 scale-100">
          <h1 className="text-3xl font-bold text-center text-gray-800 mb-6 animate-fade-in-down">
            Welcome, {user?.name || "User"}!
          </h1>
          <div className="space-y-6">
            <p className="text-center text-gray-600">
              Insira seu código Verilog e clique em "Compilar" para ver o resultado!
            </p>

            {/* Mensagem de feedback */}
            {message && (
              <p className="text-center text-sm text-gray-800 bg-gray-100 p-2 rounded-lg">
                {message}
              </p>
            )}

            {/* Editor Verilog (Colapsável, começa aberto) */}
            <div className="border rounded-lg">
              <button
                onClick={() => toggleEditor("verilog")}
                className="w-full p-3 text-black text-left font-semibold rounded-t-lg transition-all duration-300 flex justify-between items-center"
              >
                Código Verilog
                <span>{activeEditor === "verilog" ? "▲" : "▼"}</span>
              </button>
              {activeEditor === "verilog" && (
                <div className="p-4 bg-transparent items-end flex flex-col">
                                    <div className="mb-4 flex space-x-4">
                    <Button
                      onClick={() => copyToClipboard(verilogCode)}
                      variant="primario"
                      status="default"
                      className="w-full bg-gray-600 text-white py-2 rounded-lg hover:bg-gray-700 transition-all duration-300"
                    >
                      Copiar Código
                    </Button>
                    <Button
                      onClick={() => pasteFromClipboard(setVerilogCode)}
                      variant="primario"
                      status="default"
                      className="w-full bg-gray-600 text-white py-2 rounded-lg hover:bg-gray-700 transition-all duration-300"
                    >
                      Colar Código
                    </Button>
                  </div>
                  <AceEditor
                    mode="verilog"
                    theme="monokai"
                    value={verilogCode}
                    onChange={setVerilogCode}
                    name="verilog-editor"
                    editorProps={{ $blockScrolling: true }}
                    setOptions={{
                      showLineNumbers: true,
                      tabSize: 2,
                      fontSize: 14,
                    }}
                    width="100%"
                    minHeight="100px"
                    maxLines={Infinity}
                    className="rounded-lg"
                  />

                </div>
              )}
            </div>

         

            {/* Editor Python (Colapsável) */}
            {compiledResult && (
              <div className="border rounded-lg">
                <button
                  onClick={() => toggleEditor("python")}
                  className="w-full p-3  text-black text-left font-semibold rounded-t-lg  transition-all duration-300 flex justify-between items-center"
                >
                  Resultado da Compilação (Python)
                  <span>{activeEditor === "python" ? "▲" : "▼"}</span>
                </button>
                {activeEditor === "python" && (
                  <div className="p-4 bg-transparent items-end flex flex-col">
                    <div className="mb-4 flex space-x-4">
                      <Button
                        onClick={() => copyToClipboard(compiledResult)}
                        variant="primario"
                        status="default"
                        className="w-full bg-gray-600 text-white py-2 rounded-lg hover:bg-gray-700 transition-all duration-300"
                      >
                        Copiar Código
                      </Button>
                    </div>
                    <AceEditor
                      mode="python"
                      theme="monokai"
                      value={compiledResult}
                      name="python-editor"
                      editorProps={{ $blockScrolling: true }}
                      setOptions={{
                        showLineNumbers: true,
                        tabSize: 2,
                        fontSize: 14,
                        readOnly: true,
                      }}
                      width="100%"
                      minHeight="100px"
                      maxLines={Infinity}
                      className="rounded-lg"
                    />
                    
                  </div>
                )}
              </div>
            )}

            <div className="flex flex-row gap-6">
    {/* Botão Compilar */}
    <Button
              onClick={handleCompile}
              variant="primario"
              status="default"
              className="w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700 transition-all duration-300 transform hover:scale-105"
            >
              Compilar
            </Button>

            {/* Botão Logout */}
            <Button
              onClick={() => setScreen("login")}
              variant="primario"
              status="default"
              className="w-full bg-red-600 text-white py-3 rounded-lg hover:bg-red-700 transition-all duration-300 transform hover:scale-105"
            >
              Logout
            </Button>

              </div>

           
          </div>
        </div>
      )}
    </div>
  );
};

export default App;