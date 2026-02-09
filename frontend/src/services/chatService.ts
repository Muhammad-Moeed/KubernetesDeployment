// Chat API service
import { ChatRequest, ChatResponse } from '@/types/chat';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ChatService {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  /**
   * Get JWT token from localStorage session
   */
  private async getAuthToken(): Promise<string | null> {
    if (typeof window === 'undefined') return null;

    try {
      const savedSession = localStorage.getItem('session');
      if (!savedSession) return null;

      const session = JSON.parse(savedSession);
      const userId = session?.user?.id;
      const userEmail = session?.user?.email;
      const userName = session?.user?.name;

      if (!userId) return null;

      // Get JWT token from bridge endpoint
      const response = await fetch('/api/auth/jwt-token', {
        method: 'GET',
        headers: {
          'x-user-id': userId,
          ...(userEmail && { 'x-user-email': userEmail }),
          ...(userName && { 'x-user-name': userName }),
        },
        credentials: 'include',
      });

      if (response.ok) {
        const data = await response.json();
        return data?.token || null;
      }

      return null;
    } catch (error) {
      console.warn('Error getting JWT token:', error);
      return null;
    }
  }

  /**
   * Send a chat message to the backend
   */
  async sendMessage(
    userId: string,
    message: string,
    conversationId?: string | null
  ): Promise<ChatResponse> {
    const token = await this.getAuthToken();

    if (!token) {
      throw new Error('Authentication required. Please log in again.');
    }

    const requestBody: ChatRequest = {
      message,
      conversation_id: conversationId || null,
    };

    const response = await fetch(`${this.baseUrl}/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      credentials: 'include',
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({
        error: {
          code: 'UNKNOWN_ERROR',
          message: 'An unexpected error occurred',
        },
      }));

      // Handle specific error codes
      if (response.status === 401) {
        throw new Error('Your session has expired. Please log in again.');
      } else if (response.status === 403) {
        throw new Error('Access denied. Please log in again.');
      } else if (response.status === 429) {
        throw new Error('Too many requests. Please try again in a moment.');
      } else if (response.status === 503) {
        throw new Error('AI service temporarily unavailable. Please try again later.');
      }

      throw new Error(
        errorData.error?.message || `Request failed with status ${response.status}`
      );
    }

    return response.json();
  }
}

export const chatService = new ChatService(API_BASE_URL);
