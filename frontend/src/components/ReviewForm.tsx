// src/components/ReviewForm.tsx

import { useReviewForm } from "../hooks/useReviewForm";

interface ReviewFormProps {
  bathroomId: number;
}

export function ReviewForm({ bathroomId }: ReviewFormProps) {
  const {
    rating,
    setRating,
    comment,
    setComment,
    message,
    handleSubmit,
  } = useReviewForm(bathroomId);

  return (
    <div>
      <h2>Submit a Review for Bathroom {bathroomId}</h2>
      <label>
        Rating:
        <input
          type="number"
          value={rating()}
          onInput={(e) => setRating(Number(e.currentTarget.value))}
          min="1"
          max="5"
        />
      </label>
      <br />
      <label>
        Comment:
        <textarea
          value={comment()}
          onInput={(e) => setComment(e.currentTarget.value)}
        />
      </label>
      <br />
      <button onClick={handleSubmit}>Submit Review</button>
      {message() && <p>{message()}</p>}
    </div>
  );
}
