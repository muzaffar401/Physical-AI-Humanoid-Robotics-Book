/**
 * FeedbackButtons component.
 * Allows users to provide thumbs up/down feedback on responses.
 */

import React, { useState } from 'react';
import { chatClient } from '../api/chatClient';

interface FeedbackButtonsProps {
  responseId: string;
}

export function FeedbackButtons({ responseId }: FeedbackButtonsProps): JSX.Element {
  const [submitted, setSubmitted] = useState(false);
  const [rating, setRating] = useState<'positive' | 'negative' | null>(null);
  const [showFeedbackInput, setShowFeedbackInput] = useState(false);
  const [feedbackText, setFeedbackText] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleFeedback = async (newRating: 'positive' | 'negative') => {
    if (submitted) return;

    setRating(newRating);
    setError(null);

    // For negative feedback, show text input
    if (newRating === 'negative') {
      setShowFeedbackInput(true);
      return;
    }

    // For positive feedback, submit immediately
    await submitFeedback(newRating, null);
  };

  const submitFeedback = async (feedbackRating: 'positive' | 'negative', text: string | null) => {
    try {
      await chatClient.submitFeedback({
        response_id: responseId,
        rating: feedbackRating,
        feedback_text: text
      });

      setSubmitted(true);
      setShowFeedbackInput(false);

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to submit feedback';
      setError(errorMessage);
      console.error('Feedback submission error:', err);
    }
  };

  const handleSubmitText = async () => {
    if (!rating) return;
    await submitFeedback(rating, feedbackText || null);
  };

  const handleCancelText = () => {
    setShowFeedbackInput(false);
    setFeedbackText('');
    setRating(null);
  };

  if (submitted) {
    return (
      <div className="feedback-buttons submitted">
        <span className="feedback-success">✓ Thank you for your feedback!</span>
      </div>
    );
  }

  return (
    <div className="feedback-buttons">
      {!showFeedbackInput ? (
        <div className="feedback-actions">
          <button
            onClick={() => handleFeedback('positive')}
            className="feedback-button positive"
            title="This answer was helpful"
            disabled={submitted}
          >
            👍
          </button>
          <button
            onClick={() => handleFeedback('negative')}
            className="feedback-button negative"
            title="This answer could be improved"
            disabled={submitted}
          >
            👎
          </button>
        </div>
      ) : (
        <div className="feedback-input-container">
          <textarea
            value={feedbackText}
            onChange={(e) => setFeedbackText(e.target.value)}
            placeholder="How could this answer be improved? (optional)"
            className="feedback-textarea"
            rows={3}
          />
          <div className="feedback-input-actions">
            <button
              onClick={handleSubmitText}
              className="feedback-submit-button"
            >
              Submit
            </button>
            <button
              onClick={handleCancelText}
              className="feedback-cancel-button"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
      {error && <div className="feedback-error">{error}</div>}
    </div>
  );
}
