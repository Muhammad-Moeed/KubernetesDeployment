import { useState, useEffect, useCallback } from "react";

interface VoiceRecognitionResult {
  transcript: string;
  confidence: number;
}

interface UseVoiceRecognitionReturn {
  isListening: boolean;
  isSupported: boolean;
  transcript: string;
  error: string | null;
  startListening: () => void;
  stopListening: () => void;
  resetTranscript: () => void;
}

export function useVoiceRecognition(): UseVoiceRecognitionReturn {
  const [isListening, setIsListening] = useState(false);
  const [isSupported, setIsSupported] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [recognition, setRecognition] = useState<any>(null);

  useEffect(() => {
    // Check if Web Speech API is supported
    if (typeof window !== "undefined") {
      const SpeechRecognition =
        (window as any).SpeechRecognition ||
        (window as any).webkitSpeechRecognition;

      if (SpeechRecognition) {
        setIsSupported(true);
        const recognitionInstance = new SpeechRecognition();
        recognitionInstance.continuous = false;
        recognitionInstance.interimResults = false;
        recognitionInstance.lang = "en-US";
        recognitionInstance.maxAlternatives = 1;

        recognitionInstance.onresult = (event: any) => {
          const result = event.results[0][0];
          setTranscript(result.transcript);
          setError(null);
        };

        recognitionInstance.onerror = (event: any) => {
          setIsListening(false);

          switch (event.error) {
            case "no-speech":
              setError("No speech detected. Please try again.");
              break;
            case "audio-capture":
              setError("No microphone found. Please check your device.");
              break;
            case "not-allowed":
              setError("Microphone permission denied. Please allow access.");
              break;
            case "network":
              setError("Network error. Please check your connection.");
              break;
            default:
              setError("Voice recognition failed. Please try again.");
          }
        };

        recognitionInstance.onend = () => {
          setIsListening(false);
        };

        setRecognition(recognitionInstance);
      } else {
        setIsSupported(false);
        setError("Voice recognition is not supported in this browser.");
      }
    }

    return () => {
      if (recognition) {
        recognition.abort();
      }
    };
  }, []);

  const startListening = useCallback(() => {
    if (!recognition || !isSupported) {
      setError("Voice recognition is not available.");
      return;
    }

    try {
      setError(null);
      setTranscript("");
      recognition.start();
      setIsListening(true);
    } catch (err) {
      setError("Failed to start voice recognition.");
      setIsListening(false);
    }
  }, [recognition, isSupported]);

  const stopListening = useCallback(() => {
    if (recognition && isListening) {
      recognition.stop();
      setIsListening(false);
    }
  }, [recognition, isListening]);

  const resetTranscript = useCallback(() => {
    setTranscript("");
    setError(null);
  }, []);

  return {
    isListening,
    isSupported,
    transcript,
    error,
    startListening,
    stopListening,
    resetTranscript,
  };
}
