// src/components/BathroomList.tsx

import { useBathroomList } from "../hooks/useBathroomList";

export function BathroomList({ onSelect }: { onSelect: (bathroomId: number) => void }) {
  const { bathrooms, error } = useBathroomList();

  return (
    <div>
      <h2>List of Bathrooms</h2>
      {error() && <p style={{ color: "red" }}>{error()}</p>}
      <ul>
        {bathrooms().map((bathroom) => (
          <li onClick={() => onSelect(bathroom.id)} style={{ cursor: "pointer" }}>
            {bathroom.name} - {bathroom.address}
          </li>
        ))}
      </ul>
    </div>
  );
}
