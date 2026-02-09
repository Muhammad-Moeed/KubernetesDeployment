"use client";

interface MicrophoneButtonProps {
  isListening: boolean;
  isSupported: boolean;
  onStart: () => void;
  onStop: () => void;
  disabled?: boolean;
}

export function MicrophoneButton({
  isListening,
  isSupported,
  onStart,
  onStop,
  disabled = false,
}: MicrophoneButtonProps) {
  if (!isSupported) {
    return (
      <button
        type="button"
        disabled
        className="p-2 text-gray-400 cursor-not-allowed"
        title="Voice input not supported in this browser"
      >
        🎤
      </button>
    );
  }

  return (
    <button
      type="button"
      onClick={isListening ? onStop : onStart}
      disabled={disabled}
      className={`p-2 rounded-lg transition-all ${
        isListening
          ? "bg-danger text-white animate-pulse"
          : "text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
      } disabled:opacity-50 disabled:cursor-not-allowed`}
      title={isListening ? "Stop listening" : "Start voice input"}
    >
      {isListening ? (
        <span className="flex items-center gap-1">
          🎤 <span className="text-xs">Listening...</span>
        </span>
      ) : (
        "🎤"
      )}
    </button>
  );
}
