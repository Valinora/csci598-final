import { Navbar } from "../components/Navbar";
import { CreateBathroom } from "../components/CreateBathroom";
import { LoginSignup } from "../components/LoginSignup";


export default function Testpage() {
    return (
        <>
            <Navbar />
            <div>
                <h1>API Test Page</h1>
                <LoginSignup />
                <CreateBathroom />
            </div>
        </>
    )
}