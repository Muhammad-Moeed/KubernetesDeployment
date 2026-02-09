// useChat hook - Chat state management
import { useState, useCallback, useEffect } from 'react';
import { ChatMessage } from '@/types/chat';

const STORAGE_KEY = 'chat_conversation_id';
const CHAT_OPEN_KEY = 'chat_is_open';

export function useChat() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);

  // Load conversation ID from localStorage on mount
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const savedConversationId = localStorage.getItem(STORAGE_KEY);
      if (savedConversationId) {
        setConversationId(savedConversationId);
      }

      // Optionally restore chat open state
      const savedIsOpen = localStorage.getItem(CHAT_OPEN_KEY);
      if (savedIsOpen === 'true') {
        setIsOpen(true);
      }
    }
  }, []);

  // Persist conversation ID to localStorage
  const updateConversationId = useCallback((id: string) => {
    setConversationId(id);
    if (typeof window !== 'undefined') {
      localStorage.setItem(STORAGE_KEY, id);
    }
  }, []);

  // Toggle chat window
  const toggleChat = useCallback(() => {
    setIsOpen((prev) => {
      const newState = !prev;
      if (typeof window !== 'undefined') {
        localStorage.setItem(CHAT_OPEN_KEY, String(newState));
      }
      return newState;
    });
  }, []);

  // Open chat
  const openChat = useCallback(() => {
    setIsOpen(true);
    if (typeof window !== 'undefined') {
      localStorage.setItem(CHAT_OPEN_KEY, 'true');
    }
  }, []);

  // Close chat
  const closeChat = useCallback(() => {
    setIsOpen(false);
    if (typeof window !== 'undefined') {
      localStorage.setItem(CHAT_OPEN_KEY, 'false');
    }
  }, []);

  // Add a message to the chat
  const addMessage = useCallback((message: ChatMessage) => {
    setMessages((prev) => [...prev, message]);
  }, []);

  // Clear chat history
  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  // Clear conversation (on logout)
  const clearConversation = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    if (typeof window !== 'undefined') {
      localStorage.removeItem(STORAGE_KEY);
      localStorage.removeItem(CHAT_OPEN_KEY);
    }
  }, []);

  return {
    isOpen,
    messages,
    conversationId,
    toggleChat,
    openChat,
    closeChat,
    addMessage,
    clearMessages,
    updateConversationId,
    clearConversation,
  };
}
