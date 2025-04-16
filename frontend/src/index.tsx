/* @refresh reload */
import { render } from "solid-js/web";
import { lazy } from "solid-js";
import { Router } from "@solidjs/router";
import "./index.css";

const root = document.getElementById("root");

const routes = [
	{
		path: "/",
		component: lazy(() => import("./routes/Home.tsx"))
	},
	{
		path: "/about",
		component: lazy(() => import("./routes/About.tsx"))
	}
]

// biome-ignore lint/style/noNonNullAssertion: Root must exist, no valid workaround.
render(() => <Router>{routes}</Router>, root!);
