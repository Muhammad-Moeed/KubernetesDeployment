"use client";

import { useCallback } from 'react';
import { useChat } from '@/hooks/useChat';
import { useChatAPI } from '@/hooks/useChatAPI';
import { ChatIcon } from './ChatIcon';
import { ChatWindow } from './ChatWindow';
import { ChatMessage } from '@/types/chat';

/**
 * Detect if text contains RTL characters (Arabic/Urdu script)
 */
function isRTLText(text: string): boolean {
  const rtlRegex = /[\u0600-\u06FF]/;
  return rtlRegex.test(text);
}

export function ChatWidget() {
  const {
    isOpen,
    messages,
    conversationId,
    toggleChat,
    closeChat,
    addMessage,
    updateConversationId,
  } = useChat();

  const { sendMessage: sendToAPI, isLoading, error, clearError } = useChatAPI();

  /**
   * Handle sending a message
   */
  const handleSendMessage = useCallback(
    (messageText: string) => {
      // Create user message
      const userMessage: ChatMessage = {
        id: `user-${Date.now()}`,
        sender: 'user',
        text: messageText,
        timestamp: new Date(),
        isRTL: isRTLText(messageText),
      };

      // Add user message to chat
      addMessage(userMessage);

      // Send to API
      sendToAPI(messageText, conversationId, (botMessage, newConversationId) => {
        // Add bot message to chat
        addMessage(botMessage);

        // Update conversation ID if it's new
        if (newConversationId !== conversationId) {
          updateConversationId(newConversationId);
        }
      });
    },
    [conversationId, addMessage, sendToAPI, updateConversationId]
  );

  return (
    <>
      {/* Floating chat icon */}
      <ChatIcon onClick={toggleChat} isOpen={isOpen} />

      {/* Chat window */}
      {isOpen && (
        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          error={error}
          onSendMessage={handleSendMessage}
          onClose={closeChat}
          onClearError={clearError}
        />
      )}
    </>
  );
}
