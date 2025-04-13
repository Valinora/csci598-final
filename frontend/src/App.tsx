// import './App.css'
import {Navbar} from './views/Navbar.tsx';
import LoginSignup from "./views/LoginSignup.tsx";
import CreateBathroom from "./views/CreateBathroom.tsx";


function App() {
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

export default App
