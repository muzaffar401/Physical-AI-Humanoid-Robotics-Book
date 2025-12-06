/**
 * useChat hook for managing chat state.
 * Handles messages, loading state, and API interactions.
 */

import { useState, useCallback, useEffect } from 'react';
import { chatClient, ChatResponse, SourceChunk } from '../api/chatClient';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sourceChunks?: SourceChunk[];
  responseId?: string;
  timestamp: Date;
  selectedText?: string; // For displaying selected text in user messages
}

interface UseChatReturn {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  sessionId: string | null;
  sendMessage: (text: string, mode?: 'full_book' | 'selection', selectedText?: string) => Promise<void>;
  clearMessages: () => void;
  retryLastMessage: () => Promise<void>;
}

const STORAGE_KEY = 'rag-chatbot-history';
const MAX_STORED_MESSAGES = 50;

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [lastQuery, setLastQuery] = useState<{
    text: string;
    mode: 'full_book' | 'selection';
    selectedText?: string;
  } | null>(null);

  // Load messages from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        setMessages(parsed.messages.map((msg: any) => ({
          ...msg,
          timestamp: new Date(msg.timestamp)
        })));
        setSessionId(parsed.sessionId);
      }
    } catch (err) {
      console.error('Failed to load chat history:', err);
    }
  }, []);

  // Save messages to localStorage whenever they change
  useEffect(() => {
    if (messages.length > 0) {
      try {
        // Keep only last MAX_STORED_MESSAGES
        const toStore = messages.slice(-MAX_STORED_MESSAGES);
        localStorage.setItem(STORAGE_KEY, JSON.stringify({
          messages: toStore,
          sessionId
        }));
      } catch (err) {
        console.error('Failed to save chat history:', err);
      }
    }
  }, [messages, sessionId]);

  // Create session if needed
  const ensureSession = useCallback(async () => {
    if (!sessionId) {
      try {
        const session = await chatClient.createSession();
        setSessionId(session.session_id);
        return session.session_id;
      } catch (err) {
        console.error('Failed to create session:', err);
        throw err;
      }
    }
    return sessionId;
  }, [sessionId]);

  const sendMessage = useCallback(async (
    text: string,
    mode: 'full_book' | 'selection' = 'full_book',
    selectedText?: string
  ) => {
    if (!text.trim()) return;

    setError(null);
    setIsLoading(true);
    setLastQuery({ text, mode, selectedText });

    // Add user message immediately (include selectedText if in selection mode)
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: text,
      selectedText: mode === 'selection' ? selectedText : undefined,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);

    try {
      // Ensure we have a session
      const currentSessionId = await ensureSession();

      // Send query to backend
      const response: ChatResponse = await chatClient.sendQuery({
        query_text: text,
        mode,
        selected_text: selectedText || null,
        session_id: currentSessionId
      });

      // Add assistant message
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: response.response_text,
        sourceChunks: response.source_chunks,
        responseId: response.response_id,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);

      // Add error message to chat
      const errorMsg: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: `⚠️ Error: ${errorMessage}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMsg]);

    } finally {
      setIsLoading(false);
    }
  }, [ensureSession]);

  const retryLastMessage = useCallback(async () => {
    if (!lastQuery) return;
    await sendMessage(lastQuery.text, lastQuery.mode, lastQuery.selectedText);
  }, [lastQuery, sendMessage]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setSessionId(null);
    setError(null);
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  return {
    messages,
    isLoading,
    error,
    sessionId,
    sendMessage,
    clearMessages,
    retryLastMessage
  };
}
