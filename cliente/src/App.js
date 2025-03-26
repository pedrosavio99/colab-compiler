import React, { useState } from "react";
import Button from "./components/Button";
import "./index.css";

const App = () => {
  const [screen, setScreen] = useState("register"); // Tracks current screen: "register", "login", or "home"
  const [user, setUser] = useState(null); // Mock user data

  // Mock register function
  const handleRegister = (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const name = formData.get("name");
    const email = formData.get("email");
    const password = formData.get("password");
    setUser({ name, email, password });
    setScreen("login"); // Move to login screen
  };

  // Mock login function
  const handleLogin = (e) => {
    e.preventDefault();
    setScreen("home"); // Move to home screen
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center p-4">
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
        <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-lg transform transition-all duration-500 scale-100 hover:scale-105">
          <h1 className="text-3xl font-bold text-center text-gray-800 mb-6 animate-fade-in-down">
            Welcome, {user?.name || "User"}!
          </h1>
          <div className="space-y-4">
            <p className="text-center text-gray-600">
              You’ve successfully logged in! This is your dashboard.
            </p>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-indigo-100 p-4 rounded-lg text-center transform transition-all duration-300 hover:scale-105">
                <h3 className="font-semibold text-indigo-800">Profile</h3>
                <p className="text-sm text-gray-600">View your details</p>
              </div>
              <div className="bg-purple-100 p-4 rounded-lg text-center transform transition-all duration-300 hover:scale-105">
                <h3 className="font-semibold text-purple-800">Settings</h3>
                <p className="text-sm text-gray-600">Adjust preferences</p>
              </div>
            </div>
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
      )}
    </div>
  );
};

export default App;