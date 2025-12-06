/**
 * ChatWidget component - Floating chatbot widget design.
 * Professional floating widget with toggle button.
 * Updated with selection mode support (T058d)
 */

import React, { useState, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { useChat } from '../hooks/useChat';
import { useSelection } from '../hooks/useSelection';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { SelectionPopup } from './SelectionPopup';
import '../styles/chat.css';

export function ChatWidget(): JSX.Element {
  const [isOpen, setIsOpen] = useState(false);
  const [selectionMode, setSelectionMode] = useState<{
    active: boolean;
    text: string;
  }>({ active: false, text: '' });
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { messages, isLoading, error, sendMessage, clearMessages, retryLastMessage } = useChat();
  const { selectedText, selectionRect, hasSelection, clearSelection } = useSelection();

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // T058d: Handler for opening chat in selection mode
  const handleOpenWithSelection = () => {
    if (hasSelection && selectedText) {
      setSelectionMode({
        active: true,
        text: selectedText,
      });
      setIsOpen(true);
      clearSelection(); // Clear visual selection after capturing
    }
  };

  // Clear selection mode when chat is closed
  useEffect(() => {
    if (!isOpen) {
      setSelectionMode({ active: false, text: '' });
    }
  }, [isOpen]);

  const handleSubmit = async (text: string) => {
    if (selectionMode.active) {
      // T055, T056: Send in selection mode with selected text
      await sendMessage(text, 'selection', selectionMode.text);
      // Clear selection mode after sending
      setSelectionMode({ active: false, text: '' });
    } else {
      await sendMessage(text, 'full_book');
    }
  };

  const handleClearHistory = () => {
    if (confirm('Clear all chat history? This cannot be undone.')) {
      clearMessages();
      setSelectionMode({ active: false, text: '' });
    }
  };

  const widget = (
    <>
      {/* Selection Popup - T058a, T058b, T058c, T058d */}
      <SelectionPopup
        selectionRect={selectionRect}
        onAskAI={handleOpenWithSelection}
        visible={hasSelection && !isOpen}
      />

      {/* Floating Chat Button */}
      <button
        className="chat-float-button"
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
      >
        {isOpen ? (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
        ) : (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
          </svg>
        )}
        {messages.length > 0 && !isOpen && (
          <span className="chat-badge">{messages.length}</span>
        )}
      </button>

      {/* Chat Window */}
      <div className={`chat-window ${isOpen ? 'open' : ''}`}>
      <div className="chat-window-container">
        {/* Header */}
        <div className="chat-window-header">
          <div className="chat-window-title">
            <span className="chat-icon">🤖</span>
            <span>AI Assistant</span>
            {/* T055: Selection mode indicator */}
            {selectionMode.active && (
              <span className="selection-mode-badge">
                📄 Selection Mode
              </span>
            )}
          </div>
          <div className="chat-header-actions">
            <button
              onClick={handleClearHistory}
              className="chat-header-button"
              title="Clear chat history"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
              </svg>
            </button>
            <button
              onClick={() => setIsOpen(false)}
              className="chat-header-button"
              title="Close"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M18 6L6 18M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>

        {/* Content */}
        <>
            {/* Messages */}
            <div className="chat-sidebar-messages">
              {messages.length === 0 ? (
                <div className="chat-welcome">
                  <div className="welcome-icon">👋</div>
                  <h3>Hi! I'm your AI Assistant</h3>
                  <p>I can help you with questions about:</p>
                  <div className="welcome-tags">
                    <span className="tag">ROS 2</span>
                    <span className="tag">URDF</span>
                    <span className="tag">Publishers</span>
                    <span className="tag">Services</span>
                    <span className="tag">Navigation</span>
                  </div>
                  <p className="welcome-hint">Type your question below to get started</p>
                </div>
              ) : (
                <>
                  {messages.map((message) => (
                    <ChatMessage key={message.id} message={message} />
                  ))}
                  {isLoading && (
                    <div className="chat-message assistant-message loading">
                      <div className="message-avatar">🤖</div>
                      <div className="message-content">
                        <div className="typing-indicator">
                          <span></span>
                          <span></span>
                          <span></span>
                        </div>
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </>
              )}
            </div>

            {/* Error message */}
            {error && !isLoading && (
              <div className="chat-error">
                <span>⚠️ {error}</span>
                <button onClick={retryLastMessage} className="retry-button">
                  Retry
                </button>
              </div>
            )}

            {/* Input */}
            <div className="chat-window-input">
              <ChatInput
                onSubmit={handleSubmit}
                disabled={isLoading}
                placeholder={
                  isLoading
                    ? 'Thinking...'
                    : selectionMode.active
                    ? 'Ask about the selected text...'
                    : 'Ask me anything...'
                }
              />
              <div className="input-hint">
                {selectionMode.active ? (
                  <span className="selection-hint">
                    💡 Asking about selected text ({selectionMode.text.length} chars)
                  </span>
                ) : (
                  'Powered by OpenAI GPT-4'
                )}
              </div>
            </div>
          </>
        </div>
      </div>
    </>
  );

  // Render using portal to append to body
  return createPortal(widget, document.body);
}
