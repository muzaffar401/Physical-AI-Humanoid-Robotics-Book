/**
 * ChatInput component.
 * Text input with submit button for sending messages.
 */

import React, { useState, KeyboardEvent } from 'react';

interface ChatInputProps {
  onSubmit: (text: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export function ChatInput({
  onSubmit,
  disabled = false,
  placeholder = "Ask a question about the book..."
}: ChatInputProps): JSX.Element {
  const [input, setInput] = useState('');

  const handleSubmit = () => {
    const trimmed = input.trim();
    if (trimmed && !disabled) {
      onSubmit(trimmed);
      setInput('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="chat-input-container">
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        className="chat-input"
        disabled={disabled}
        rows={2}
      />
      <button
        onClick={handleSubmit}
        disabled={disabled || !input.trim()}
        className="chat-submit-button"
        title="Send message (Enter)"
      >
        Send
      </button>
    </div>
  );
}
