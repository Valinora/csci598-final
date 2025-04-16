// import './App.css'
import { Navbar } from '../components/Navbar.tsx';
import LoginSignup from "../components/LoginSignup.tsx";
import CreateBathroom from "../components/CreateBathroom.tsx";


export default function App() {
    return (
        <>
            <Navbar />
            <div>
                <h1>Bathroom Review App</h1>
                <LoginSignup />
                <CreateBathroom />
            </div>
        </>
    );
}