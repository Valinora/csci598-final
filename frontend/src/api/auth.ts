// /frontend/src/api/auth.ts

export async function signup(username: string, password: string) {
  const token = localStorage.getItem("access");
  console.log("Signup Token:", token);
  const response = await fetch(`/api/signup/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Signup failed.");
  }

  return data;
}

export async function login(username: string, password: string) {
  const token = localStorage.getItem("access");
  console.log("Login Token:", token);
  const response = await fetch(`/api/login/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Login failed.");
  }

  return data;
}

  