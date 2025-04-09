/* @refresh reload */
import { render } from "solid-js/web";
import { Navbar } from "./Navbar.tsx";
import "./index.css";

function Home() {
	return <Navbar active="About" />;
}

const root = document.getElementById("root");

// biome-ignore lint/style/noNonNullAssertion: Root must exist, no valid workaround.
render(() => <Home />, root!);
