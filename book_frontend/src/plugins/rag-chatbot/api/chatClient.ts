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
  private readonly REQUEST_TIMEOUT = 60000; // 60 seconds for Render cold starts
  private readonly MAX_RETRIES = 3;
  private readonly RETRY_DELAY = 2000; // 2 seconds

  constructor(baseUrl: string = API_BASE_URL) {
    // Normalize baseUrl: remove trailing slashes and ensure clean URL
    this.baseUrl = baseUrl.replace(/\/+$/, '').trim();
  }

  /**
   * Helper to build URLs without double slashes
   */
  private buildUrl(path: string): string {
    // Ensure path starts with / and baseUrl doesn't end with /
    const cleanPath = path.startsWith('/') ? path : `/${path}`;
    return `${this.baseUrl}${cleanPath}`;
  }

  /**
   * Fetch with timeout and retry logic for Render cold starts
   */
  private async fetchWithRetry(
    url: string,
    options: RequestInit,
    retries: number = this.MAX_RETRIES
  ): Promise<Response> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.REQUEST_TIMEOUT);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });
      clearTimeout(timeoutId);
      return response;
    } catch (error) {
      clearTimeout(timeoutId);

      // If it's a network error and we have retries left, retry
      if (
        (error instanceof TypeError || error instanceof DOMException) &&
        retries > 0
      ) {
        // Wait before retrying (exponential backoff)
        const delay = this.RETRY_DELAY * (this.MAX_RETRIES - retries + 1);
        await new Promise((resolve) => setTimeout(resolve, delay));
        return this.fetchWithRetry(url, options, retries - 1);
      }

      throw error;
    }
  }

  /**
   * Create a new chat session.
   */
  async createSession(userIdentifier?: string): Promise<SessionCreateResponse> {
    try {
      const response = await this.fetchWithRetry(this.buildUrl('/api/session'), {
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
      if (error instanceof TypeError || error instanceof DOMException) {
        if (error.message.includes('aborted') || error.message.includes('timeout')) {
          throw new Error(
            `Backend request timed out. The Render free tier service may be spinning up. ` +
            `Please try again in a moment.`
          );
        }
        throw new Error(
          `Cannot connect to backend API at ${this.baseUrl}. ` +
          `The service may be starting up. Please wait and try again. Error: ${error.message}`
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
      const response = await this.fetchWithRetry(this.buildUrl('/api/chat'), {
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
      if (error instanceof TypeError || error instanceof DOMException) {
        if (error.message.includes('aborted') || error.message.includes('timeout')) {
          throw new Error(
            `Backend request timed out. The Render free tier service may be spinning up ` +
            `(this can take 30-60 seconds after inactivity). Please try again in a moment.`
          );
        }
        throw new Error(
          `Cannot connect to backend API at ${this.baseUrl}. ` +
          `The service may be starting up (Render free tier cold starts take 30-60 seconds). ` +
          `Please wait a moment and try again. Error: ${error.message}`
        );
      }
      throw error;
    }
  }

  /**
   * Submit feedback for a response.
   */
  async submitFeedback(request: FeedbackRequest): Promise<void> {
    const response = await this.fetchWithRetry(this.buildUrl('/api/feedback'), {
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
      const response = await this.fetchWithRetry(this.buildUrl('/api/health'), {
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
      if (error instanceof TypeError || error instanceof DOMException) {
        if (error.message.includes('aborted') || error.message.includes('timeout')) {
          throw new Error(
            `Backend health check timed out. The Render free tier service may be spinning up. ` +
            `Please try again in a moment.`
          );
        }
        throw new Error(
          `Cannot connect to backend API at ${this.baseUrl}. ` +
          `The service may be starting up. Please wait and try again. Error: ${error.message}`
        );
      }
      throw error;
    }
  }
}

// Singleton instance
export const chatClient = new ChatClient();
