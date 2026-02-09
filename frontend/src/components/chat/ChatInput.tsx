"use client";

import { useState, KeyboardEvent, useRef, useEffect } from 'react';
import { VoiceButton } from './VoiceButton';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

/**
 * Detect if text contains RTL characters (Arabic/Urdu script)
 */
function isRTLText(text: string): boolean {
  const rtlRegex = /[\u0600-\u06FF]/;
  return rtlRegex.test(text);
}

export function ChatInput({
  onSendMessage,
  disabled = false,
  placeholder = 'Type a message...',
}: ChatInputProps) {
  const [message, setMessage] = useState('');
  const [detectedLanguage, setDetectedLanguage] = useState<'en-US' | 'ur-PK'>('en-US');
  const inputRef = useRef<HTMLInputElement>(null);

  // Focus input on mount
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  // Detect language from input text
  useEffect(() => {
    if (message.trim()) {
      const isUrdu = isRTLText(message);
      setDetectedLanguage(isUrdu ? 'ur-PK' : 'en-US');
    }
  }, [message]);

  const handleSend = () => {
    const trimmedMessage = message.trim();
    if (trimmedMessage && !disabled) {
      onSendMessage(trimmedMessage);
      setMessage('');
      // Refocus input after sending
      setTimeout(() => {
        if (inputRef.current) {
          inputRef.current.focus();
        }
      }, 100);
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleVoiceTranscript = (transcript: string) => {
    setMessage(transcript);
    // Auto-send after voice input
    setTimeout(() => {
      if (transcript.trim()) {
        onSendMessage(transcript.trim());
        setMessage('');
      }
    }, 500);
  };

  // Dynamic placeholder based on detected language
  const dynamicPlaceholder = detectedLanguage === 'ur-PK'
    ? 'پیغام لکھیں...'
    : placeholder;

  return (
    <div className="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 p-4">
      <div className="flex items-center gap-2">
        {/* Voice button with language detection */}
        <VoiceButton
          onTranscript={handleVoiceTranscript}
          disabled={disabled}
          language={detectedLanguage}
        />

        {/* Text input */}
        <input
          ref={inputRef}
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={dynamicPlaceholder}
          disabled={disabled}
          maxLength={1000}
          className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white disabled:opacity-50 disabled:cursor-not-allowed"
          aria-label="Chat message input"
          dir={isRTLText(message) ? 'rtl' : 'ltr'}
        />

        {/* Send button */}
        <button
          onClick={handleSend}
          disabled={disabled || !message.trim()}
          className="p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          aria-label="Send message"
        >
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M14 5l7 7m0 0l-7 7m7-7H3"
            />
          </svg>
        </button>
      </div>
    </div>
  );
}
