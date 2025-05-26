"""Camera management for video capture operations."""
import cv2
import base64
import numpy as np
from typing import Optional, Tuple
from config import CameraConfig


class CameraManager:
    """Manages camera operations and frame processing."""

    def __init__(self, config: CameraConfig):
        self.config = config
        self.video: Optional[cv2.VideoCapture] = None
        self.camera_index: Optional[int] = None

    def initialize(self) -> bool:
        """Initialize camera connection."""
        for idx in self.config.indices_to_try:
            self.video = cv2.VideoCapture(idx)
            if self.video.isOpened():
                self.camera_index = idx
                print(f"📷 Camera opened successfully (index: {idx})")
                self._configure_camera()
                return True

        print("❌ Error: Could not open camera")
        return False

    def _configure_camera(self) -> None:
        """Configure camera properties."""
        if self.video:
            self.video.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.width)
            self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.height)

    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Read a frame from the camera."""
        if not self.video:
            return False, None
        return self.video.read()

    def resize_frame(self, frame: np.ndarray, target_size: int) -> np.ndarray:
        """Resize frame maintaining aspect ratio."""
        height, width = frame.shape[:2]

        if width <= target_size and height <= target_size:
            return frame

        # Calculate aspect ratio
        aspect = width / height
        if aspect > 1:
            new_width = target_size
            new_height = int(target_size / aspect)
        else:
            new_height = target_size
            new_width = int(target_size * aspect)

        return cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

    def encode_frame(self, frame: np.ndarray, quality: int = 85) -> str:
        """Encode frame to base64 string."""
        _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
        return base64.b64encode(buffer).decode("utf-8")

    def add_overlay(self, frame: np.ndarray, instruction_count: int) -> np.ndarray:
        """Add text overlay to frame."""
        cv2.putText(frame, "AI Director Active", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Instructions given: {instruction_count}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)
        return frame

    def show_frame(self, frame: np.ndarray, window_name: str = 'AI Director View (Press Q to stop)') -> None:
        """Display frame in window."""
        cv2.imshow(window_name, frame)

    def check_quit(self) -> bool:
        """Check if quit key was pressed."""
        return cv2.waitKey(1) & 0xFF == ord('q')

    def release(self) -> None:
        """Release camera resources."""
        if self.video:
            self.video.release()
        cv2.destroyAllWindows()

    def __enter__(self):
        """Context manager entry."""
        if self.initialize():
            return self
        raise RuntimeError("Failed to initialize camera")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.release() 