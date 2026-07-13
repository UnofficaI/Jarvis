"""Text-to-Speech module for Jarvis"""

import pyttsx3
from typing import Optional


class TextToSpeech:
    """Convert text to speech using pyttsx3"""

    def __init__(self, rate: int = 150, volume: float = 0.9):
        """Initialize Text-to-Speech engine

        Args:
            rate: Speech rate (words per minute), default 150
            volume: Volume level (0.0 to 1.0), default 0.9
        """
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)

    def speak(self, text: str) -> None:
        """Convert text to speech and play it

        Args:
            text: Text to speak
        """
        try:
            print(f"🔊 Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"❌ Error speaking: {e}")

    def set_voice(self, voice_id: int = 0) -> None:
        """Set the voice to use

        Args:
            voice_id: Voice ID (0 for male, 1 for female, etc.)
        """
        try:
            voices = self.engine.getProperty("voices")
            if voice_id < len(voices):
                self.engine.setProperty("voice", voices[voice_id].id)
                print(f"✅ Voice set to {voices[voice_id].name}")
            else:
                print(f"❌ Voice ID {voice_id} not available")
        except Exception as e:
            print(f"❌ Error setting voice: {e}")

    def set_rate(self, rate: int) -> None:
        """Set speech rate

        Args:
            rate: Speech rate in words per minute
        """
        try:
            self.engine.setProperty("rate", rate)
            print(f"✅ Speech rate set to {rate} words per minute")
        except Exception as e:
            print(f"❌ Error setting rate: {e}")

    def set_volume(self, volume: float) -> None:
        """Set speech volume

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        try:
            if 0.0 <= volume <= 1.0:
                self.engine.setProperty("volume", volume)
                print(f"✅ Volume set to {volume}")
            else:
                print("❌ Volume must be between 0.0 and 1.0")
        except Exception as e:
            print(f"❌ Error setting volume: {e}")

    def get_available_voices(self) -> list:
        """Get list of available voices

        Returns:
            List of available voices
        """
        try:
            voices = self.engine.getProperty("voices")
            return [(i, voice.name) for i, voice in enumerate(voices)]
        except Exception as e:
            print(f"❌ Error getting voices: {e}")
            return []
