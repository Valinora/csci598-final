// /frontend/src/api/review.ts

export interface Review {
  bathroomId: number;
  rating: number;
  comment: string;
}

export async function submitReview(review: Review) {
  const token = localStorage.getItem("access");

  try {
    const response = await fetch(`/api/bathrooms/${review.bathroomId}/reviews/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: token ? `Bearer ${token}` : "",
      },
      body: JSON.stringify({
        bathroom: review.bathroomId,
        rating: review.rating,
        comment: review.comment,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      console.error("Error response:", error); // Log error content
      throw new Error(error?.detail || "Failed to submit review");
    }

    return response.json();
  } catch (err) {
    console.error("Error during review submission:", err);
    throw new Error(err instanceof Error ? err.message : "Unknown error");
  }
}
