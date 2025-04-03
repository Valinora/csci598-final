// import { createSignal } from "solid-js";

interface NavbarProps {
    active: string
}

export function Navbar(props: NavbarProps) {



    return (
        <nav class = "navbar" >
            <a href="/index.html">Home</a>
        </nav>
    )

}