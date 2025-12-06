/**
 * ChatMessage component.
 * Displays a single message (user or assistant) with markdown support.
 */

import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Message } from '../hooks/useChat';
import { CitationLink } from './CitationLink';
import { FeedbackButtons } from './FeedbackButtons';

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps): JSX.Element {
  const isUser = message.role === 'user';

  return (
    <div className={`chat-message ${isUser ? 'user-message' : 'assistant-message'}`}>
      <div className="message-avatar">
        {isUser ? '👤' : '🤖'}
      </div>
      <div className="message-content">
        {/* Show selected text for user messages in selection mode */}
        {isUser && message.selectedText && (
          <div className="message-selected-text">
            <div className="selected-text-label">📄 Selected text:</div>
            <blockquote className="selected-text-content">
              {message.selectedText}
            </blockquote>
          </div>
        )}

        <div className="message-text">
          {isUser ? (
            <p>{message.content}</p>
          ) : (
            <ReactMarkdown>{message.content}</ReactMarkdown>
          )}
        </div>

        {/* Show citations for assistant messages with sources */}
        {!isUser && message.sourceChunks && message.sourceChunks.length > 0 && (
          <div className="message-citations">
            <div className="citations-label">Sources:</div>
            <div className="citations-list">
              {message.sourceChunks.map((chunk, index) => (
                <CitationLink key={chunk.chunk_id} chunk={chunk} index={index} />
              ))}
            </div>
          </div>
        )}

        {/* Show feedback buttons for assistant messages */}
        {!isUser && message.responseId && (
          <div className="message-feedback">
            <FeedbackButtons responseId={message.responseId} />
          </div>
        )}

        <div className="message-timestamp">
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  );
}
