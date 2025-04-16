import { createSignal } from "solid-js";
import { useAuth } from "../hooks/useAuth";

export default function LoginSignup() {
  const [username, setUsername] = createSignal("");
  const [password, setPassword] = createSignal("");
  const { handleLogin, handleSignup, message } = useAuth();

  return (
    <div style={{ "max-width": "400px", margin: "auto", padding: "1rem" }}>
      <h2>Login / Signup</h2>
      <input
        type="text"
        placeholder="Username"
        value={username()}
        onInput={(e) => setUsername(e.currentTarget.value)}
      /><br />
      <input
        type="password"
        placeholder="Password"
        value={password()}
        onInput={(e) => setPassword(e.currentTarget.value)}
      /><br />
      <button type="button" onClick={() => handleLogin(username(), password())}>Login</button>
      <button type="button" onClick={() => handleSignup(username(), password())}>Signup</button>
      <p>{message()}</p>
    </div>
  );
}
