"""AI Director - Core choreographic direction logic."""
import time
from typing import List, Optional
from openai import OpenAI
from config import DIRECTOR_PROMPT, DirectorConfig
from audio_manager import AudioManager


class AIDirector:
    """AI Director that analyzes scenes and provides choreographic instructions."""

    def __init__(self, openai_client: OpenAI, audio_manager: AudioManager, config: DirectorConfig):
        self.openai_client = openai_client
        self.audio_manager = audio_manager
        self.config = config
        self.last_instruction = ""
        self.instruction_count = 0

    def analyze_scene(self, frames: List[str]) -> Optional[str]:
        """Analyze frames and generate director instructions."""
        if not frames:
            return None

        messages = [
            {
                "role": "user",
                "content": [
                    DIRECTOR_PROMPT,
                    *[{"image": frame, "resize": self.config.image_size} for frame in frames],
                ],
            },
        ]

        try:
            result = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=100,
            )
            return result.choices[0].message.content
        except Exception as e:
            print(f"❌ Error analyzing scene: {e}")
            return None

    def give_instruction(self, instruction: str) -> bool:
        """Give a voice instruction if it's different from the last one."""
        if instruction and instruction != self.last_instruction:
            timestamp = time.strftime('%H:%M:%S')
            print(f"\n🎭 Director ({timestamp}): {instruction}")

            if self.audio_manager.speak(instruction):
                self.last_instruction = instruction
                self.instruction_count += 1
                return True

        return False

    def process_frames(self, frames: List[str]) -> bool:
        """Process frames and give instruction if needed."""
        instruction = self.analyze_scene(frames)
        if instruction:
            return self.give_instruction(instruction)
        return False

    def get_stats(self) -> dict:
        """Get director statistics."""
        return {
            "instruction_count": self.instruction_count,
            "last_instruction": self.last_instruction
        } 