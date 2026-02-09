"use client";

import { useEffect, useRef } from 'react';
import { ChatMessage as ChatMessageType } from '@/types/chat';
import { Message } from './Message';

interface MessageListProps {
  messages: ChatMessageType[];
  isLoading?: boolean;
}

export function MessageList({ messages, isLoading = false }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isLoading]);

  // Welcome message when no conversation history
  const showWelcome = messages.length === 0 && !isLoading;

  return (
    <div
      ref={containerRef}
      className="flex-1 overflow-y-auto px-4 py-4 space-y-2"
      style={{ maxHeight: 'calc(100% - 130px)' }}
    >
      {showWelcome && (
        <div className="flex items-center justify-center h-full">
          <div className="text-center max-w-md px-6 py-8 bg-gray-50 dark:bg-gray-800 rounded-xl">
            <div className="text-4xl mb-4">💬</div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Welcome to AI Assistant
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              I can help you manage your tasks. Try saying:
            </p>
            <ul className="mt-4 text-sm text-gray-700 dark:text-gray-300 space-y-2 text-left">
              <li className="flex items-start">
                <span className="mr-2">➕</span>
                <span>&quot;Add a task to buy groceries&quot;</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">📋</span>
                <span>&quot;Show me all my tasks&quot;</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">✅</span>
                <span>&quot;Mark task 2 as done&quot;</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">✏️</span>
                <span>&quot;Update task 1 title to new name&quot;</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">🎯</span>
                <span>&quot;Set task 3 priority to high&quot;</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">🗑️</span>
                <span>&quot;Delete task 4&quot;</span>
              </li>
            </ul>
          </div>
        </div>
      )}

      {messages.map((message) => (
        <Message key={message.id} message={message} />
      ))}

      {/* Loading indicator (typing animation) */}
      {isLoading && (
        <div className="flex justify-start mb-4">
          <div className="bg-gray-100 dark:bg-gray-800 px-4 py-3 rounded-2xl rounded-bl-sm">
            <div className="flex space-x-2">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
            </div>
          </div>
        </div>
      )}

      {/* Scroll anchor */}
      <div ref={messagesEndRef} />
    </div>
  );
}
