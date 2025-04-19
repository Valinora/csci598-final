// src/components/Navbar.tsx

import { type routesLiteral, routes } from "../index.tsx";


// Type level programming to keep this interface up to date.
export interface NavbarProps {
	active?: typeof routesLiteral[number]["name"];
}

export function Navbar(props: NavbarProps) {
	const navlist = [];

	// Building the list of routes dynamically at runtime is probably bad, but I don't want to hardcode navpages
	// until after we actually know what pages we want the navbar to have. Until then, generate all of them.
	for (const page of routes) {
		let linkClasses = "nav-link text-light";

		if (props.active === page.name) {
			linkClasses += " active";
		}

		navlist.push(
			<li class="nav-item">
				<a class={linkClasses} href={page.path}>
					{page.name}
				</a>
			</li>,
		);
	}

	return (
		<nav class="navbar navbar-expand bg-dark">
			<ul class="navbar-nav mr-auto">
				<div class="collapse navbar-collapse">{navlist}</div>
			</ul>
		</nav>
	);
}
