// /frontend/src/routes/Testing.tsx

import { createSignal } from "solid-js";
import { Navbar } from "../components/Navbar";
import { CreateBathroom } from "../components/CreateBathroom";
import { LoginSignup } from "../components/LoginSignup";
import { BathroomList } from "../components/BathroomList";
import { ReviewForm } from "../components/ReviewForm";

export default function TestPage() {
  const [selectedBathroom, setSelectedBathroom] = createSignal<number | null>(null);

  const handleBathroomSelect = (bathroomId: number) => {
    setSelectedBathroom(bathroomId);
  };

  return (
    <>
      <Navbar />
      <div>
        <h1>API Test Page</h1>
        <LoginSignup />
        <CreateBathroom />
        <BathroomList onSelect={handleBathroomSelect} />
        {selectedBathroom() && <ReviewForm bathroomId={selectedBathroom()!} />}
      </div>
    </>
  );
}
