// src/hooks/useBathroomList.ts

import { createSignal, onMount } from "solid-js";
import { getBathrooms } from "../api/bathroom";

export function useBathroomList() {
  const [bathrooms, setBathrooms] = createSignal<any[]>([]);
  const [error, setError] = createSignal<string>("");

  const fetchBathrooms = async () => {
    try {
      const fetchedBathrooms = await getBathrooms();
      setBathrooms(fetchedBathrooms);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      }
    }
  };

  onMount(fetchBathrooms);

  return { bathrooms, error, refetch: fetchBathrooms };
}
