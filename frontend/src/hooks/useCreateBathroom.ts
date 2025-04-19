// src/hooks/useCreateBathroom.ts

import { createSignal } from "solid-js";
import { createBathroom } from "../api/bathroom";

export function useCreateBathroom() {
  const [error, setError] = createSignal("");
  const [success, setSuccess] = createSignal(false);

  const handleCreate = async () => {
    try {
      const newBathroom = await createBathroom({
        name: "Union Station Restroom",
        address: "700 Main St, Metropolis",
        latitude: 38.8951,
        longitude: -77.0364,
        rating: 4.0,
      });
      console.log("Created bathroom:", newBathroom);
      setSuccess(true);
      setError("");
    } catch (err) {
      if (err instanceof Error) {
        setSuccess(false);
        setError(err.message);
      }
    }
  };

  return {
    handleCreate,
    success,
    error,
  };
}
