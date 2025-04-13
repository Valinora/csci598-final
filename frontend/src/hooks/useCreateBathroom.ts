// src/hooks/useCreateBathroom.ts
import { createSignal } from "solid-js";
import { createBathroom } from "../api/bathroom";

export function useCreateBathroom() {
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

  return {
    handleCreate,
    success,
    error,
  };
}
