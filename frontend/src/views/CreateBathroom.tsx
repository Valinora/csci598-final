// src/CreateBathroom.tsx

import { createSignal } from "solid-js";
import { createBathroom } from "../api";

export default function CreateBathroom() {
  const [error, setError] = createSignal<string | null>(null);
  const [success, setSuccess] = createSignal<boolean>(false);

  const handleCreate = async () => {
    try {
      const newBathroom = await createBathroom({
        name: "Union Station Restroom",
        address: "700 Main St, Metropolis",
        latitude: 38.8951,
        longitude: -77.0364,
      });

      console.log("Created bathroom:", newBathroom);
      setSuccess(true);
      setError(null);
    } catch (err: any) {
      setSuccess(false);
      setError(err.message);
    }
  };

  return (
    <div>
      <h2>Create Bathroom</h2>
      <button onClick={handleCreate}>Submit Sample Bathroom</button>
      {success() && <p style={{ color: "green" }}>Success!</p>}
      {error() && <p style={{ color: "red" }}>{error()}</p>}
    </div>
  );
}
