/* @refresh reload */
import { render } from "solid-js/web";
import { App } from "./App.tsx";
import "./index.css";

const root = document.getElementById("root");

// biome-ignore lint/style/noNonNullAssertion: Root must exist, no valid workaround.
render(() => <App />, root!);
