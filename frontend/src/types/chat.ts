// Chat type definitions

export interface ChatMessage {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  timestamp: Date;
  isRTL?: boolean;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string | null;
}

export interface ChatResponse {
  success: boolean;
  response: string;
  conversation_id: string;
  timestamp: string;
}

export interface ChatError {
  error: {
    code: string;
    message: string;
    details?: string;
  };
}
