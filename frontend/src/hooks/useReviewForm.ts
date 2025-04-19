// /frontend/src/hooks/useReviewForm.ts

import { createSignal } from "solid-js";
import { submitReview } from "../api/review";

export function useReviewForm(bathroomId: number) {
  const [rating, setRating] = createSignal(0);
  const [comment, setComment] = createSignal("");
  const [message, setMessage] = createSignal("");

  const handleSubmit = async () => {
    const review = {
      bathroomId,
      rating: rating(),
      comment: comment(),
    };

    try {
      await submitReview(review);
      setMessage("Review submitted successfully!");
      setRating(0);
      setComment("");
    } catch (err) {
      if (err instanceof Error) {
        setMessage(err.message);
      }
    }
  };

  return {
    rating,
    setRating,
    comment,
    setComment,
    message,
    handleSubmit,
  };
}
