// useChatAPI hook - API integration for chat
import { useState, useCallback } from 'react';
import { useAuth } from '@/contexts/auth-context';
import { chatService } from '@/services/chatService';
import { ChatMessage } from '@/types/chat';

/**
 * Detect if text contains RTL characters (Arabic/Urdu script)
 */
function isRTLText(text: string): boolean {
  // Unicode range for Arabic/Urdu: U+0600 to U+06FF
  const rtlRegex = /[\u0600-\u06FF]/;
  return rtlRegex.test(text);
}

export function useChatAPI() {
  const { user } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Send a message to the chat API
   */
  const sendMessage = useCallback(
    async (
      message: string,
      conversationId: string | null,
      onSuccess: (botMessage: ChatMessage, newConversationId: string) => void
    ) => {
      if (!user?.id) {
        setError('User not authenticated');
        return;
      }

      if (!message.trim()) {
        setError('Message cannot be empty');
        return;
      }

      setIsLoading(true);
      setError(null);

      try {
        const response = await chatService.sendMessage(
          user.id,
          message.trim(),
          conversationId
        );

        // Create bot message from response
        const botMessage: ChatMessage = {
          id: `bot-${Date.now()}`,
          sender: 'bot',
          text: response.response,
          timestamp: new Date(response.timestamp),
          isRTL: isRTLText(response.response),
        };

        // Call success callback with bot message and conversation ID
        onSuccess(botMessage, response.conversation_id);
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : 'Failed to send message';
        setError(errorMessage);
        console.error('Chat API error:', err);
      } finally {
        setIsLoading(false);
      }
    },
    [user?.id]
  );

  /**
   * Clear error state
   */
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    sendMessage,
    isLoading,
    error,
    clearError,
  };
}
