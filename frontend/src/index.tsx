/* @refresh reload */
import { render } from "solid-js/web";
import { lazy } from "solid-js";
import { Router } from "@solidjs/router";
import "./index.css";

const root = document.getElementById("root");

export const routesLiteral = [
	{
		path: "/",
		name: "Home",
		component: lazy(() => import("./routes/Home.tsx"))
	},
	{
		path: "/about",
		name: "About",
		component: lazy(() => import("./routes/About.tsx"))
	},
	{
		path: "/apitest",
		name: "API Test",
		component: lazy(() => import("./routes/Testing.tsx"))
	}
] as const;

// Some shuffling to get around `as const`.
export const routes = [...routesLiteral];

// biome-ignore lint/style/noNonNullAssertion: Root must exist, no valid workaround.
render(() => <Router>{routes}</Router>, root!);
