"""API client management for OpenAI and ElevenLabs."""
import sys
from typing import Optional
from openai import OpenAI
from elevenlabs import ElevenLabs
from config import APIConfig


class APIClientManager:
    """Manages API client initialization and validation."""

    def __init__(self, config: APIConfig):
        self.config = config
        self._openai_client: Optional[OpenAI] = None
        self._elevenlabs_client: Optional[ElevenLabs] = None

    @property
    def openai_client(self) -> OpenAI:
        """Get or create OpenAI client."""
        if not self._openai_client:
            if not self.config.openai_key:
                raise ValueError("OpenAI API key not configured")
            self._openai_client = OpenAI(api_key=self.config.openai_key)
        return self._openai_client

    @property
    def elevenlabs_client(self) -> ElevenLabs:
        """Get or create ElevenLabs client."""
        if not self._elevenlabs_client:
            if not self.config.elevenlabs_key:
                raise ValueError("ElevenLabs API key not configured")
            self._elevenlabs_client = ElevenLabs(api_key=self.config.elevenlabs_key)
        return self._elevenlabs_client

    def validate_openai_key(self) -> bool:
        """Validate OpenAI API key by making a test request."""
        print("🔍 Validating OpenAI API key...")
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            print("✅ OpenAI API key is valid")
            return True
        except Exception as e:
            print(f"❌ OpenAI API key validation failed: {e}")
            return False

    def validate_elevenlabs_key(self) -> bool:
        """Validate ElevenLabs API key by checking available voices."""
        print("🔍 Validating ElevenLabs API key...")
        try:
            voices_response = self.elevenlabs_client.voices.get_all()
            available_voices = voices_response.voices
            if available_voices:
                print(f"✅ ElevenLabs API key is valid ({len(available_voices)} voices available)")
                return True
            else:
                print("❌ ElevenLabs API key validation failed: No voices available")
                return False
        except Exception as e:
            print(f"❌ ElevenLabs API key validation failed: {e}")
            return False

    def validate_all_keys(self) -> bool:
        """Validate all required API keys."""
        print("\n🔐 Validating API Keys...")
        print("-" * 40)

        # First check if keys are present
        valid, errors = self.config.validate()
        if not valid:
            print("\n❌ API key validation failed!")
            for error in errors:
                print(f"  • {error}")
            print("\nPlease check your .env file and ensure your API keys are correct.")
            print("\nRequired format in .env file:")
            print("OPENAI_API_KEY=sk-...")
            print("ELEVENLABS_API_KEY=...")
            return False

        # Then validate the keys work
        openai_valid = self.validate_openai_key()
        elevenlabs_valid = self.validate_elevenlabs_key()

        print("-" * 40)

        if not openai_valid or not elevenlabs_valid:
            print("\n❌ API key validation failed!")
            return False

        print("\n✅ All API keys validated successfully!")
        return True 