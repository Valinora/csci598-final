// src/api/bathroom.ts

export interface Bathroom {
  name: string,
  address: string,
  latitude: number,
  longitude: number,
  rating: number; // Ensure this line is added
}
// Create bathroom function for testing
export async function createBathroom(data: Bathroom) {
  const token = localStorage.getItem("access");

  const response = await fetch('/api/bathrooms/', {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: token ? `Bearer ${token}` : "",
    },
    body: JSON.stringify({
      ...data,
      rating: data.rating ?? 0.0,
      created_at: new Date().toISOString(),
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error?.detail || "Failed to create bathroom");
  }

  return response.json();
}

// Fetch bathroom list for testing
export async function getBathrooms() {
  const response = await fetch('/api/bathrooms/', {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error?.detail || "Failed to fetch bathrooms");
  }

  return response.json();
}


  