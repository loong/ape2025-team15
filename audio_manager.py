"""Audio management for text-to-speech operations."""
import os
import tempfile
import pygame
from typing import Optional
from elevenlabs import ElevenLabs
from config import AudioConfig


class AudioManager:
    """Manages audio playback and text-to-speech conversion."""

    def __init__(self, client: ElevenLabs, voice_id: str, config: AudioConfig):
        self.client = client
        self.voice_id = voice_id
        self.config = config
        self._initialize_pygame()

    def _initialize_pygame(self) -> None:
        """Initialize pygame mixer for audio playback."""
        pygame.mixer.init()

    def speak(self, text: str) -> bool:
        """Convert text to speech and play it."""
        try:
            # Generate audio using ElevenLabs
            audio_response = self.client.text_to_speech.convert(
                voice_id=self.voice_id,
                text=text,
                model_id=self.config.model_id,
                voice_settings={
                    "stability": self.config.stability,
                    "similarity_boost": self.config.similarity_boost,
                    "style": self.config.style,
                    "use_speaker_boost": self.config.use_speaker_boost
                },
                output_format=self.config.output_format
            )

            # Save and play audio
            self._play_audio_stream(audio_response)
            return True

        except Exception as e:
            print(f"❌ Error generating speech: {e}")
            return False

    def _play_audio_stream(self, audio_stream) -> None:
        """Play audio from stream."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            # Write audio chunks to file
            for chunk in audio_stream:
                tmp_file.write(chunk)
            tmp_file_path = tmp_file.name

        try:
            # Play the audio file
            pygame.mixer.music.load(tmp_file_path)
            pygame.mixer.music.play()

            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)

    def stop(self) -> None:
        """Stop any currently playing audio."""
        pygame.mixer.music.stop()

    def __del__(self):
        """Cleanup pygame mixer."""
        pygame.mixer.quit() 