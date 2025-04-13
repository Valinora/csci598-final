// src/LoginSignup.tsx
import { createSignal } from "solid-js";

export default function LoginSignup() {
  const [username, setUsername] = createSignal("");
  const [password, setPassword] = createSignal("");
  const [message, setMessage] = createSignal("");

  const handleSignup = async () => {
    try {
      const response = await fetch(`/api/signup/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          username: username(),
          password: password()
        })
      });

      const data = await response.json();
      if (response.ok) {
        setMessage("Signup successful!");
      } else {
        setMessage(data.error || "Signup failed.");
      }
    } catch (err) {
      setMessage("Error connecting to server.");
    }
  };

  const handleLogin = async () => {
    try {
      const response = await fetch(`/api/login/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username: username(), password: password() }),
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.detail || "Login failed.");
        return;
      }

      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
      setMessage("Login successful!");
    } catch (err) {
      setMessage("Error connecting to server.");
    }
  };

  return (
    <div style={{ "max-width": "400px", margin: "auto", padding: "1rem" }}>
      <h2>Login / Signup</h2>
      <input
        name="password"
        type="text"
        placeholder="Username"
        value={username()}
        onInput={(e) => setUsername(e.currentTarget.value)}
        style={{ "margin-bottom": "0.5rem", width: "100%" }}
      /><br />
      <input
        name="password"
        type="password"
        placeholder="Password"
        value={password()}
        onInput={(e) => setPassword(e.currentTarget.value)}
        style={{ "margin-bottom": "0.5rem", width: "100%" }}
      /><br />
      <button onClick={handleLogin} style={{ "margin-right": "0.5rem" }}>Login</button>
      <button onClick={handleSignup}>Signup</button>
      <p>{message()}</p>
    </div>
  );
}
