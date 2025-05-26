"""User interface module for AI Director."""
from config import DirectorConfig


class UserInterface:
    """Handles user interface and interactions."""

    def show_welcome(self) -> None:
        """Display welcome message."""
        print("🎬 AI Film Director")
        print("=" * 40)
        print("Your personal AI director will watch through the camera")
        print("and provide real-time voice feedback to improve your shots!")
        print("=" * 40)

    def get_director_config(self) -> DirectorConfig:
        """Get director configuration from user input."""
        print("\n⚙️  Configuration")
        print("-" * 40)

        # Get FPS
        fps_input = input("Analysis frequency in FPS (default: 0.3): ").strip()
        fps = float(fps_input) if fps_input else 0.3

        # Get frames per analysis
        frames_input = input("Frames per analysis (default: 1): ").strip()
        frames = int(frames_input) if frames_input else 1

        # Get image size
        size_input = input("Image size for OpenAI processing (default: 512, min: 256): ").strip()
        image_size = int(size_input) if size_input else 512

        config = DirectorConfig(
            fps=fps,
            frames_per_analysis=frames,
            image_size=image_size
        )

        return config.validate()

    def show_session_info(self, config: DirectorConfig) -> None:
        """Display session information."""
        print(f"\n🎬 AI Director is ready!")
        print(f"📊 Analyzing every {config.frames_per_analysis} frames at {config.fps} fps")
        print(f"🖼️  Image size for OpenAI: {config.image_size}x{config.image_size} pixels")
        print("Press 'q' to stop")
        print("-" * 40)

    def show_session_summary(self, stats: dict) -> None:
        """Display session summary."""
        print(f"\n✅ Director gave {stats['instruction_count']} instructions")
        if stats['last_instruction']:
            print(f"📝 Last instruction: {stats['last_instruction'][:50]}...") 