// src/hooks/useAuth.ts
import { createSignal } from "solid-js";
import { login, signup } from "../api/auth";

export function useAuth() {
  const [message, setMessage] = createSignal("");

  const handleSignup = async (username: string, password: string) => {
    try {
      await signup(username, password);
      setMessage("Signup successful!");
    } catch (err: any) {
      setMessage(err.message || "Signup failed.");
    }
  };

  const handleLogin = async (username: string, password: string) => {
    try {
      const data = await login(username, password);
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
      setMessage("Login successful!");
    } catch (err: any) {
      setMessage(err.message || "Login failed.");
    }
  };

  return {
    handleSignup,
    handleLogin,
    message,
  };
}
