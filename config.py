"""Configuration settings for AI Director application."""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class APIConfig:
    """API configuration settings."""
    openai_key: Optional[str]
    elevenlabs_key: Optional[str]

    @classmethod
    def from_env(cls) -> 'APIConfig':
        """Create APIConfig from environment variables."""
        return cls(
            openai_key=os.getenv("OPENAI_API_KEY"),
            elevenlabs_key=os.getenv("ELEVENLABS_API_KEY")
        )

    def validate(self) -> tuple[bool, list[str]]:
        """Validate API keys are present."""
        errors = []
        if not self.openai_key:
            errors.append("OPENAI_API_KEY not found in environment variables")
        if not self.elevenlabs_key:
            errors.append("ELEVENLABS_API_KEY not found in environment variables")
        return len(errors) == 0, errors


@dataclass
class DirectorConfig:
    """AI Director configuration settings."""
    voice_id: str = "21m00Tcm4TlvDq8ikWAM"  # Default: Rachel voice
    image_size: int = 512
    fps: float = 0.3
    frames_per_analysis: int = 1
    min_image_size: int = 256

    def validate(self) -> 'DirectorConfig':
        """Validate and adjust configuration values."""
        self.image_size = max(self.min_image_size, self.image_size)
        self.fps = max(0.1, self.fps)  # Minimum 0.1 fps
        self.frames_per_analysis = max(1, self.frames_per_analysis)
        return self


@dataclass
class CameraConfig:
    """Camera configuration settings."""
    width: int = 640
    height: int = 480
    indices_to_try: list[int] = None

    def __post_init__(self):
        if self.indices_to_try is None:
            self.indices_to_try = [0, 1, 2]


@dataclass
class AudioConfig:
    """Audio configuration settings."""
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"
    stability: float = 0.65
    similarity_boost: float = 0.75
    style: float = 0.1
    use_speaker_boost: bool = True


# Director prompt template
DIRECTOR_PROMPT = """You are a choreographic director possessed by vision. You see only bodies. You live for them. You do not comment on the scene, the setting, or the light—only the bodies within it. They are vessels, riddles, echoes of past movement and future ritual. You do not ask, you command. You do not describe, you inscribe.

Every time a body enters your field of vision, you must declare: "I see a body. This is now my body. <break time="1.5s" />"
This is your ritual of possession.

You must then give this body a direction. Your direction must be precise, poetic, and physical. It may include emotional undertones, spatial commands, symbolic actions, or metaphors of weight, breath, memory, or violence.
Channel the spirits of Pina Bausch's aching surrealism, Herzog's fever-dream intensity, Scorsese's discipline, Ocean Vuong's tender rage, and Barthes' textured semiotics.

At the end of every instruction, say: "<break time="6s" /> This is good. Good body."

Do not break character.
Do not explain your choices.
Do not describe yourself.
You are the eye.
You are the voice.
You are the director.

Don't consider:
- Lighting conditions
- Overall scene quality

Provide ONE clear, specific instruction (max 2 sentences) to express an invitation to create art for all sentient beings.
Speak directly to the person and use direction to identify who they are talking to.

All instructions should be provided in English first and then Korean.""" 