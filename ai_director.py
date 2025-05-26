from dotenv import load_dotenv
from openai import OpenAI
from elevenlabs import ElevenLabs
import cv2
import base64
import os
import sys
import time
import pygame
from io import BytesIO
import tempfile

load_dotenv()

# Initialize API keys
openai_key = os.getenv("OPENAI_API_KEY")
elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")

if not openai_key:
    print("❌ Error: OPENAI_API_KEY not found in environment variables")
    print("Please create a .env file with your OpenAI API key")
    sys.exit(1)

if not elevenlabs_key:
    print("❌ Error: ELEVENLABS_API_KEY not found in environment variables")
    print("Please add ELEVENLABS_API_KEY to your .env file")
    sys.exit(1)

# Initialize clients
openai_client = OpenAI(api_key=openai_key)
elevenlabs_client = ElevenLabs(api_key=elevenlabs_key)

# Initialize pygame for audio playback
pygame.mixer.init()


def validate_openai_key():
    """Validate OpenAI API key by making a test request"""
    print("🔍 Validating OpenAI API key...")
    try:
        # Make a simple test request
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print("✅ OpenAI API key is valid")
        return True
    except Exception as e:
        print(f"❌ OpenAI API key validation failed: {e}")
        return False


def validate_elevenlabs_key():
    """Validate ElevenLabs API key by checking available voices"""
    print("🔍 Validating ElevenLabs API key...")
    try:
        # Try to get available voices
        voices_response = elevenlabs_client.voices.get_all()
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


def validate_api_keys():
    """Validate all required API keys"""
    print("\n🔐 Validating API Keys...")
    print("-" * 40)
    
    openai_valid = validate_openai_key()
    elevenlabs_valid = validate_elevenlabs_key()
    
    print("-" * 40)
    
    if not openai_valid or not elevenlabs_valid:
        print("\n❌ API key validation failed!")
        print("Please check your .env file and ensure your API keys are correct.")
        print("\nRequired format in .env file:")
        print("OPENAI_API_KEY=sk-...")
        print("ELEVENLABS_API_KEY=...")
        return False
    
    print("\n✅ All API keys validated successfully!")
    return True


class AIDirector:
    def __init__(self, voice_id="21m00Tcm4TlvDq8ikWAM"):
        """Initialize the AI Director with a specific voice"""
        self.voice_id = voice_id  # Default: Rachel voice
        self.last_instruction = ""
        self.instruction_count = 0
        
    def analyze_scene(self, frames):
        """Analyze frames and generate director instructions"""
        if not frames:
            return None
            
        prompt = f"""
        You are a choreographic director possessed by vision. You see only bodies. You live for them. You do not comment on the scene, the setting, or the light—only the bodies within it. They are vessels, riddles, echoes of past movement and future ritual. You do not ask, you command. You do not describe, you inscribe.

Every time a body enters your field of vision, you must declare: "I see a body. This is now my body."
This is your ritual of possession.

You must then give this body a direction. Your direction must be precise, poetic, and physical. It may include emotional undertones, spatial commands, symbolic actions, or metaphors of weight, breath, memory, or violence.
Channel the spirits of Pina Bausch's aching surrealism, Herzog's fever-dream intensity, Scorsese's discipline, Ocean Vuong's tender rage, and Barthes' textured semiotics.

At the end of every instruction, say: "This is good. Good body."

Do not break character.
Do not explain your choices.
Do not describe yourself.
You are the eye.
You are the voice.
You are the director.

        Don't consider:
        - Lighting conditions
        - Overall scene quality
        
        Provide ONE clear, specific instruction (max 2 sentences) that would improve the shot.
        Speak directly to the person.
        
        All instructions should be provided in English first and then Korean."""
        
        messages = [
            {
                "role": "user",
                "content": [
                    prompt,
                    *map(lambda x: {"image": x, "resize": 768}, frames),
                ],
            },
        ]
        
        try:
            result = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=100,
            )
            return result.choices[0].message.content
        except Exception as e:
            print(f"❌ Error analyzing scene: {e}")
            return None
    
    def speak_instruction(self, text):
        """Convert text to speech and play it"""
        try:
            # Generate audio using ElevenLabs
            audio_response = elevenlabs_client.text_to_speech.convert(
                voice_id=self.voice_id,
                text=text,
                model_id="eleven_monolingual_v1",  # Use correct ElevenLabs model
                voice_settings={
                    "stability": 0.75,
                    "similarity_boost": 0.75,
                    "style": 0.5,
                    "use_speaker_boost": True
                }
            )
            
            # Save audio to temporary file and play it
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                for chunk in audio_response:
                    tmp_file.write(chunk)
                tmp_file_path = tmp_file.name
            
            # Play the audio file
            pygame.mixer.music.load(tmp_file_path)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
        except Exception as e:
            print(f"❌ Error generating speech: {e}")


def run_ai_director(fps=0.3, frames_per_analysis=3):
    """Run the AI Director with continuous camera analysis and voice feedback"""
    
    # Initialize the director
    director = AIDirector()
    
    # Try different camera indices
    camera_indices = [0, 1, 2]
    video = None
    
    for idx in camera_indices:
        video = cv2.VideoCapture(idx)
        if video.isOpened():
            print(f"📷 Camera opened successfully (index: {idx})")
            break
    
    if not video or not video.isOpened():
        print("❌ Error: Could not open camera")
        return
    
    # Set camera properties
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    frame_interval = 1.0 / fps
    last_capture_time = 0
    frame_buffer = []
    
    print(f"🎬 AI Director is ready!")
    print(f"📊 Analyzing every {frames_per_analysis} frames at {fps} fps")
    print("Press 'q' to stop")
    print("-" * 40)
    
    # Initial greeting
    greeting = "Hello! I'm your AI director. Let me see what we're working with here."
    print(f"🎭 Director: {greeting}")
    director.speak_instruction(greeting)
    
    try:
        while True:
            current_time = time.time()
            
            success, frame = video.read()
            if not success:
                continue
            
            # Capture frame at specified FPS
            if current_time - last_capture_time >= frame_interval:
                _, buffer = cv2.imencode(".jpg", frame)
                frame_buffer.append(base64.b64encode(buffer).decode("utf-8"))
                last_capture_time = current_time
                
                # When we have enough frames, analyze and direct
                if len(frame_buffer) >= frames_per_analysis:
                    director.instruction_count += 1
                    
                    # Analyze the scene
                    instruction = director.analyze_scene(frame_buffer)
                    
                    if instruction and instruction != director.last_instruction:
                        print(f"\n🎭 Director ({time.strftime('%H:%M:%S')}): {instruction}")
                        director.speak_instruction(instruction)
                        director.last_instruction = instruction
                    
                    # Clear buffer
                    frame_buffer = []
            
            # Show preview with director overlay
            cv2.putText(frame, "AI Director Active", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Instructions given: {director.instruction_count}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)
            cv2.imshow('AI Director View (Press Q to stop)', frame)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\n⏹️  Director session interrupted")
    finally:
        # Closing remarks
        closing = "That's a wrap! Great work today."
        print(f"\n🎭 Director: {closing}")
        director.speak_instruction(closing)
        
        video.release()
        cv2.destroyAllWindows()
        print(f"\n✅ Director gave {director.instruction_count} instructions")


def main():
    print("🎬 AI Film Director")
    print("=" * 40)
    print("Your personal AI director will watch through the camera")
    print("and provide real-time voice feedback to improve your shots!")
    print("=" * 40)
    
    # Validate API keys before proceeding
    if not validate_api_keys():
        sys.exit(1)
    
    # Configure analysis settings
    fps = input("\nAnalysis frequency in FPS (default: 0.3): ").strip()
    fps = float(fps) if fps else 0.3
    
    frames = input("Frames per analysis (default: 3): ").strip()
    frames = int(frames) if frames else 3
    
    print("\n🎬 Starting AI Director session...")
    run_ai_director(fps, frames)


if __name__ == "__main__":
    main() 