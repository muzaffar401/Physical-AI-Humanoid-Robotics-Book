/**
 * API client for RAG chatbot backend.
 * Handles all HTTP requests to the FastAPI backend.
 */

const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://rag-chatbot-api-lr57.onrender.com'
  : 'http://localhost:8000';

export interface ChatQueryRequest {
  query_text: string;
  mode: 'full_book' | 'selection';
  selected_text?: string | null;
  session_id?: string | null;
}

export interface SourceChunk {
  chunk_id: string;
  module_number: number;
  chapter_number: number;
  section_title: string;
  url: string;
  score: number;
}

export interface ChatResponse {
  response_id: string;
  response_text: string;
  source_chunks: SourceChunk[];
  response_time_ms: number;
  session_id: string;
}

export interface FeedbackRequest {
  response_id: string;
  rating: 'positive' | 'negative';
  feedback_text?: string | null;
}

export interface SessionCreateResponse {
  session_id: string;
  created_at: string;
}

class ChatClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Create a new chat session.
   */
  async createSession(userIdentifier?: string): Promise<SessionCreateResponse> {
    const response = await fetch(`${this.baseUrl}/api/session`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_identifier: userIdentifier }),
    });

    if (!response.ok) {
      throw new Error(`Failed to create session: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Send a chat query and get response.
   */
  async sendQuery(request: ChatQueryRequest): Promise<ChatResponse> {
    const response = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      if (response.status === 429) {
        throw new Error('Rate limit exceeded. Please wait a moment and try again.');
      }
      if (response.status === 400) {
        const error = await response.json();
        throw new Error(error.detail || 'Invalid request');
      }
      throw new Error(`Failed to send query: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Submit feedback for a response.
   */
  async submitFeedback(request: FeedbackRequest): Promise<void> {
    const response = await fetch(`${this.baseUrl}/api/feedback`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      if (response.status === 409) {
        throw new Error('Feedback already submitted for this response');
      }
      throw new Error(`Failed to submit feedback: ${response.statusText}`);
    }
  }

  /**
   * Check API health.
   */
  async healthCheck(): Promise<{ status: string; version: string }> {
    const response = await fetch(`${this.baseUrl}/api/health`);

    if (!response.ok) {
      throw new Error('API health check failed');
    }

    return response.json();
  }
}

// Singleton instance
export const chatClient = new ChatClient();
