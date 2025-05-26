# AI Director 🎬

An AI-powered choreographic director that provides real-time voice feedback through camera analysis. The system uses OpenAI's GPT-4 Vision for scene analysis and ElevenLabs for text-to-speech conversion.

## Features

- 🎥 Real-time camera analysis
- 🗣️ Voice feedback using ElevenLabs TTS
- 🎭 Poetic, artistic direction inspired by renowned directors
- 🌐 Multilingual support (English and Korean)
- ⚙️ Configurable analysis parameters

## Project Structure

```
.
├── main.py              # Main entry point
├── config.py            # Configuration classes and constants
├── api_clients.py       # API client management
├── camera_manager.py    # Camera operations
├── audio_manager.py     # Audio/TTS operations
├── ai_director.py       # Core AI director logic
├── ui.py               # User interface
├── requirements.txt     # Python dependencies
└── .env                # Environment variables (create this)
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd team15-voice
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```env
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...
```

## Usage

Run the application:
```bash
python main.py
```

The application will:
1. Validate your API keys
2. Ask for configuration parameters
3. Start the camera and begin analysis
4. Provide voice feedback based on what it sees
5. Press 'q' to quit

## Configuration Options

- **FPS**: Analysis frequency (default: 0.3)
- **Frames per analysis**: Number of frames to analyze together (default: 1)
- **Image size**: Resolution for OpenAI processing (default: 512, min: 256)

## Architecture

### Modular Design

The refactored code follows a modular architecture with clear separation of concerns:

- **Config Module**: Centralized configuration management using dataclasses
- **API Clients**: Manages OpenAI and ElevenLabs client initialization
- **Camera Manager**: Handles all camera operations and frame processing
- **Audio Manager**: Manages text-to-speech and audio playback
- **AI Director**: Core logic for scene analysis and instruction generation
- **UI Module**: User interface and interaction handling
- **Main Module**: Orchestrates the entire application flow

### Key Improvements

1. **Better Error Handling**: Each module has proper error handling and validation
2. **Type Hints**: Full type annotations for better code clarity
3. **Context Managers**: Camera resources are properly managed
4. **Configuration Validation**: Input validation with sensible defaults
5. **Separation of Concerns**: Each module has a single, clear responsibility

## Requirements

- Python 3.8+
- OpenCV (cv2)
- OpenAI API with GPT-4 Vision access
- ElevenLabs API
- pygame (for audio playback)

## API Keys

You'll need:
- OpenAI API key with GPT-4 Vision access
- ElevenLabs API key for text-to-speech
