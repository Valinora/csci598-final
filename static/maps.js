// Check if the browser supports geolocation
if ("geolocation" in navigator) {
	// Request geolocation permissions
	navigator.geolocation.getCurrentPosition(
		(position) => {
			// Success callback: Write position data to the div with id "coords"
			const coordsDiv = document.getElementById("coords");
			coordsDiv.innerText = `
                    Latitude: ${position.coords.latitude}
                    Longitude: ${position.coords.longitude}
                    Accuracy: ${position.coords.accuracy} meters
                    Altitude: ${position.coords.altitude || "N/A"}
                    Altitude Accuracy: ${position.coords.altitudeAccuracy || "N/A"} meters
                    Heading: ${position.coords.heading || "N/A"}
                    Speed: ${position.coords.speed || "N/A"} m/s
                    Timestamp: ${new Date(position.timestamp).toLocaleString()}
                `;
		},
		(error) => {
			// Error callback: Handle errors
			const coordsDiv = document.getElementById("coords");
			coordsDiv.innerText = `Error: ${error.message}`;
		},
	);
} else {
	// Geolocation is not supported
	const coordsDiv = document.getElementById("coords");
	coordsDiv.innerText = "Geolocation is not supported by your browser.";
}
