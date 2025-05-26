"""Main entry point for AI Director application."""
import sys
import time
from typing import List
from config import APIConfig, DirectorConfig, CameraConfig, AudioConfig
from api_clients import APIClientManager
from camera_manager import CameraManager
from audio_manager import AudioManager
from ai_director import AIDirector
from ui import UserInterface


class DirectorSession:
    """Manages a complete AI Director session."""

    def __init__(self):
        self.ui = UserInterface()
        self.api_config = APIConfig.from_env()
        self.api_manager = APIClientManager(self.api_config)
        self.director_config = None
        self.camera_config = CameraConfig()
        self.audio_config = AudioConfig()

    def setup(self) -> bool:
        """Setup and validate the session."""
        self.ui.show_welcome()

        # Validate API keys
        if not self.api_manager.validate_all_keys():
            return False

        # Get user configuration
        self.director_config = self.ui.get_director_config()
        return True

    def run(self) -> None:
        """Run the director session."""
        # Initialize components
        audio_manager = AudioManager(
            self.api_manager.elevenlabs_client,
            self.director_config.voice_id,
            self.audio_config
        )

        director = AIDirector(
            self.api_manager.openai_client,
            audio_manager,
            self.director_config
        )

        # Run camera session
        try:
            with CameraManager(self.camera_config) as camera:
                self._run_camera_loop(camera, director)
        except RuntimeError as e:
            print(f"❌ {e}")
            return

    def _run_camera_loop(self, camera: CameraManager, director: AIDirector) -> None:
        """Run the main camera processing loop."""
        frame_interval = 1.0 / self.director_config.fps
        last_capture_time = 0
        frame_buffer: List[str] = []

        self.ui.show_session_info(self.director_config)

        try:
            while True:
                current_time = time.time()

                success, frame = camera.read_frame()
                if not success:
                    continue

                # Capture frame at specified FPS
                if current_time - last_capture_time >= frame_interval:
                    # Process and encode frame
                    resized_frame = camera.resize_frame(frame, self.director_config.image_size)
                    encoded_frame = camera.encode_frame(resized_frame)
                    frame_buffer.append(encoded_frame)
                    last_capture_time = current_time

                    # Analyze when we have enough frames
                    if len(frame_buffer) >= self.director_config.frames_per_analysis:
                        director.process_frames(frame_buffer)
                        frame_buffer = []

                # Show preview with overlay
                frame_with_overlay = camera.add_overlay(frame, director.instruction_count)
                camera.show_frame(frame_with_overlay)

                # Check for quit
                if camera.check_quit():
                    break

        except KeyboardInterrupt:
            print("\n⏹️  Director session interrupted")
        finally:
            stats = director.get_stats()
            self.ui.show_session_summary(stats)


def main():
    """Main entry point."""
    session = DirectorSession()

    if session.setup():
        print("\n🎬 Starting AI Director session...")
        session.run()
    else:
        sys.exit(1)


if __name__ == "__main__":
    main() 