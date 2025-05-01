document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".star-rating-container").forEach(container => {
        const avg = parseFloat(container.dataset.average);
        const userRating = parseInt(container.dataset.user || 0);
        const stars = container.querySelectorAll(".hover-star i");
  
        const applyStars = (val, isUser = false) => {
            stars.forEach((star, index) => {
                const starNum = index + 1;
                star.className = "fa-solid fa-star text-warning";
  
                if (val >= starNum) {
                    star.style.opacity = isUser ? 1.0 : 0.95;
                } else if (val >= starNum - 0.5) {
                    star.style.opacity = isUser ? 0.7 : 0.6;
                } else {
                    star.style.opacity = isUser ? 0.4 : 0.25;
                }
            });
        };
        applyStars(avg);
  
        stars.forEach((star, index) => {
            const hoverVal = index + 1;
  
            star.parentElement.addEventListener("mouseenter", () => {
                applyStars(hoverVal, true);
            });
            star.parentElement.addEventListener("mouseleave", () => {
                applyStars(avg);
            });
        });
    });
});
  