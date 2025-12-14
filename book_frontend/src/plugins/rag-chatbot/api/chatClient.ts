/**
 * API client for RAG chatbot backend.
 * Handles all HTTP requests to the FastAPI backend.
 */

const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://chatbot-rag-krlg.onrender.com'
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
    // Remove trailing slash if present to avoid double slashes in URLs
    this.baseUrl = baseUrl.replace(/\/+$/, '');
  }

  /**
   * Create a new chat session.
   */
  async createSession(userIdentifier?: string): Promise<SessionCreateResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_identifier: userIdentifier }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        let errorMessage = `Failed to create session: ${response.status} ${response.statusText}`;
        try {
          const errorJson = JSON.parse(errorText);
          errorMessage = errorJson.detail || errorMessage;
        } catch {
          if (errorText) errorMessage += ` - ${errorText}`;
        }
        throw new Error(errorMessage);
      }

      return response.json();
    } catch (error) {
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error(
          `Cannot connect to backend API at ${this.baseUrl}. ` +
          `Please ensure the backend server is running. ` +
          `Error: ${error.message}`
        );
      }
      throw error;
    }
  }

  /**
   * Send a chat query and get response.
   */
  async sendQuery(request: ChatQueryRequest): Promise<ChatResponse> {
    try {
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
        
        const errorText = await response.text();
        let errorMessage = `Failed to send query: ${response.status} ${response.statusText}`;
        
        try {
          const errorJson = JSON.parse(errorText);
          errorMessage = errorJson.detail || errorMessage;
        } catch {
          if (errorText) errorMessage += ` - ${errorText}`;
        }
        
        if (response.status === 400) {
          throw new Error(errorMessage);
        }
        throw new Error(errorMessage);
      }

      return response.json();
    } catch (error) {
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error(
          `Cannot connect to backend API at ${this.baseUrl}. ` +
          `Please ensure the backend server is running on port 8000. ` +
          `Error: ${error.message}`
        );
      }
      throw error;
    }
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
    try {
      const response = await fetch(`${this.baseUrl}/api/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`API health check failed: ${response.status} ${response.statusText}`);
      }

      return response.json();
    } catch (error) {
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error(
          `Cannot connect to backend API at ${this.baseUrl}. ` +
          `Please ensure the backend server is running. ` +
          `Error: ${error.message}`
        );
      }
      throw error;
    }
  }
}

// Singleton instance
export const chatClient = new ChatClient();
