// import { createSignal } from "solid-js";

export const PageMap = {
	Home: "/",
	About: "/about",
};

export interface NavbarProps {
	active?: keyof typeof PageMap;
}

export function Navbar(props: NavbarProps) {
	const navlist = [];

	for (const [name, dest] of Object.entries(PageMap)) {
		let linkClasses = "nav-link text-light";

		if (props.active === name) {
			linkClasses += " active";
		}

		navlist.push(
			<li class="nav-item">
				<a class={linkClasses} href={dest}>
					{name}
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
