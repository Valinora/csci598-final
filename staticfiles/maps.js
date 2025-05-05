// Function to handle geolocation
function findLocation() {
    const button = document.getElementById("location-btn");
    const spinner = document.getElementById("spinner");

    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                button.disabled = false;
                spinner.style.display = "none";
                button.innerText = "Find Nearby Bathrooms";

                button.addEventListener("click", () => {
                    window.location.href = `/nearby?lat=${encodeURIComponent(latitude)}&long=${encodeURIComponent(longitude)}`;
                });
            },
            (error) => {
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
        alert("Geolocation is not supported by your browser.");
        button.disabled = false;
        spinner.style.display = "none";
        button.innerText = "Geolocation Not Supported";
    }
}

// Start finding location immediately upon page load
document.addEventListener("DOMContentLoaded", findLocation);