"""Speech Recognition module for Jarvis"""

import speech_recognition as sr
from typing import Optional


class VoiceRecognizer:
    """Recognize voice commands using Google Speech Recognition API"""

    def __init__(self):
        """Initialize Voice Recognizer"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self, timeout: int = 10, phrase_time_limit: int = None) -> Optional[str]:
        """Listen to microphone and convert speech to text

        Args:
            timeout: Maximum time to wait for input in seconds
            phrase_time_limit: Maximum time for a single phrase in seconds

        Returns:
            Recognized text or None if recognition failed
        """
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

            # Recognize speech using Google Speech Recognition
            print("🧠 Processing...")
            text = self.recognizer.recognize_google(audio)
            print(f"✅ You said: {text}")
            return text.lower()

        except sr.UnknownValueError:
            print("❌ Sorry, I couldn't understand what you said.")
            return None
        except sr.RequestError as e:
            print(f"❌ Could not request results: {e}")
            return None
        except sr.WaitTimeoutError:
            print("❌ No input detected. Please try again.")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def listen_for_keyword(
        self, keyword: str, timeout: int = 30, max_attempts: int = 5
    ) -> bool:
        """Listen for a specific keyword

        Args:
            keyword: Keyword to listen for
            timeout: Maximum time to wait in seconds
            max_attempts: Maximum number of attempts

        Returns:
            True if keyword detected, False otherwise
        """
        attempts = 0
        while attempts < max_attempts:
            recognized_text = self.listen(timeout=timeout)
            if recognized_text and keyword.lower() in recognized_text:
                return True
            attempts += 1
        return False
