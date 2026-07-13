"""Voice Assistant for Jarvis with command processing"""

from .speech_recognition import VoiceRecognizer
from .text_to_speech import TextToSpeech
from typing import Callable, Dict, Optional


class VoiceAssistant:
    """Voice-controlled assistant for Jarvis"""

    def __init__(self, name: str = "Jarvis", voice_id: int = 0):
        """Initialize Voice Assistant

        Args:
            name: Name of the assistant
            voice_id: Voice ID to use (0 for male, 1 for female)
        """
        self.name = name
        self.recognizer = VoiceRecognizer()
        self.speaker = TextToSpeech()
        self.speaker.set_voice(voice_id)
        self.commands: Dict[str, Callable] = {}
        self.running = False

    def register_command(self, keywords: list, callback: Callable) -> None:
        """Register a voice command

        Args:
            keywords: List of keywords that trigger this command
            callback: Function to call when command is detected
        """
        for keyword in keywords:
            self.commands[keyword.lower()] = callback

    def process_command(self, text: str) -> None:
        """Process a voice command

        Args:
            text: Recognized text to process
        """
        if not text:
            return

        # Check if any command keyword is in the recognized text
        for keyword, callback in self.commands.items():
            if keyword in text:
                try:
                    callback(text)
                except Exception as e:
                    self.speaker.speak(f"Error executing command: {e}")
                return

        # If no command found
        self.speaker.speak(f"Sorry, I don't understand that command. Please try again.")

    def listen_and_process(self, continuous: bool = False) -> None:
        """Listen for voice commands and process them

        Args:
            continuous: If True, keep listening in a loop
        """
        self.running = True
        self.speaker.speak(f"Hello! I'm {self.name}. How can I help you?")

        try:
            if continuous:
                while self.running:
                    text = self.recognizer.listen()
                    if text:
                        if "stop" in text or "exit" in text:
                            self.speaker.speak("Goodbye!")
                            self.running = False
                            break
                        self.process_command(text)
            else:
                text = self.recognizer.listen()
                if text:
                    self.process_command(text)
        except KeyboardInterrupt:
            self.speaker.speak("Goodbye!")
            self.running = False

    def greet(self) -> None:
        """Greet the user"""
        self.speaker.speak(f"Hello! I'm {self.name}. Ready to assist.")

    def stop(self) -> None:
        """Stop the assistant"""
        self.running = False
        self.speaker.speak("Shutting down.")
