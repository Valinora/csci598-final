// Function to handle geolocation
function findLocation() {
    const button = document.getElementById("location-btn");
    const spinner = document.getElementById("spinner");

    // Check if the browser supports geolocation
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                // Success: Enable the button and update its text
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                button.disabled = false;
                spinner.style.display = "none";
                button.innerText = "Find Nearby Bathrooms";

                // Attach click event to redirect to /nearby with lat and long as query parameters
                button.addEventListener("click", () => {
                    window.location.href = `/nearby?lat=${encodeURIComponent(latitude)}&long=${encodeURIComponent(longitude)}`;
                });
            },
            (error) => {
                // Error: Display error message
                console.log(error);
                button.disabled = false;
                spinner.style.display = "none";
                button.innerText = "Retry Finding Location";

                button.addEventListener("click", () => {
                  window.location = window.location.href;
                })
            }
        );
    } else {
        // Geolocation not supported
        alert("Geolocation is not supported by your browser.");
        button.disabled = false;
        spinner.style.display = "none";
        button.innerText = "Geolocation Not Supported";
    }
}

// Start finding location immediately upon page load
document.addEventListener("DOMContentLoaded", findLocation);