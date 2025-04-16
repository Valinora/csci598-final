import { useCreateBathroom } from "../hooks/useCreateBathroom";

export default function CreateBathroom() {
  const { handleCreate, success, error } = useCreateBathroom();

  return (
    <div>
      <h2>Create Bathroom</h2>
      <button type="button" onClick={handleCreate}>Submit Sample Bathroom</button>
      {success() && <p style={{ color: "green" }}>Success!</p>}
      {error() && <p style={{ color: "red" }}>{error()}</p>}
    </div>
  );
}
