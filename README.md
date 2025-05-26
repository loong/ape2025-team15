# Video Analysis Tool with OpenAI GPT-4 Vision

This tool analyzes video content using OpenAI's GPT-4 Vision API. It can process both video files and live camera feeds.

## Features

- 📹 Analyze video files with customizable frame sampling
- 📷 Capture and analyze live camera feed
- 🤖 Use GPT-4 Vision to describe video content
- 🎯 Custom prompts for specific analysis needs
- 🎬 **NEW**: AI Film Director with voice feedback using ElevenLabs

## Setup

### 1. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

Replace with your actual API keys:
- Get OpenAI API key from: https://platform.openai.com/api-keys
- Get ElevenLabs API key from: https://elevenlabs.io/

### 4. Validate API Keys (Optional but Recommended)

Test your API keys before running the main applications:

```bash
python test_api_keys.py
```

This will verify that both your OpenAI and ElevenLabs API keys are valid and working.

## Usage

### Video Analyzer

```bash
python video_analyzer.py
```

#### Options:

1. **Analyze Video File**
   - Provide path to video file
   - Set frame sampling rate (default: every 30th frame)
   - Optionally provide custom analysis prompt

2. **Analyze Camera Feed**
   - Set recording duration (default: 5 seconds)
   - Set capture FPS (default: 1 frame per second)
   - Press 'Q' to stop recording early
   - Optionally provide custom analysis prompt

3. **Continuous Camera Analysis**
   - Camera stays open continuously
   - Analyzes frames in real-time
   - Configurable FPS and frames per analysis
   - Press 'Q' to stop

### AI Film Director (NEW!)

```bash
python ai_director.py
```

The AI Director watches through your camera and provides real-time voice feedback to improve your shots!

#### Features:
- 🎭 Multiple director personalities (encouraging, professional, artistic, strict)
- 🗣️ Natural voice synthesis using ElevenLabs
- 📊 Real-time scene analysis
- 🎬 Continuous feedback loop

#### Director Personalities:
1. **Encouraging** - Supportive and positive feedback
2. **Professional** - Technical and precise instructions
3. **Artistic** - Creative and experimental suggestions
4. **Strict** - Demanding perfection in every shot

### Example Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Run the standard analyzer
python video_analyzer.py

# Or run the AI Director
python ai_director.py

# Follow the prompts to configure your session
```

## Requirements

- Python 3.8+
- OpenAI API key with GPT-4 Vision access
- ElevenLabs API key (for AI Director)
- Camera access (for live feed modes)
- Video file (for file analysis mode)

## Notes

- The tool samples frames to reduce API costs
- Camera feed captures frames at specified FPS for the duration
- Adjust frame sampling/capture rates based on your needs and API limits
- AI Director provides voice feedback at configurable intervals

## Author

Long Hoang 