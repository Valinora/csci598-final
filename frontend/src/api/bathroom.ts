export interface Bathroom {
  name: string,
  address: string,
  latitude: number,
  longitude: number,
}

export async function createBathroom(data: Bathroom) {
    const token = localStorage.getItem("access");
  
    const response = await fetch('/api/bathrooms/', {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: token ? `Bearer ${token}` : "",
      },
      body: JSON.stringify(data),
    });
  
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error?.detail || "Failed to create bathroom");
    }
  
    return response.json();
  }
  