# AI Theatre Director

An AI-powered choreographic director that watches through your camera and provides real-time voice feedback to guide your movement and performance.

## Team

This project was build during the APE Camp in Seoul organized by the Korean Arts Council in 2025.

Team members:
 - [Halim Madi](https://www.instagram.com/yalla_halim/) (Artist)
 - [Gyuwon Lee](https://www.instagram.com/gwsylvia) (Artist)
 - [Hyunjin Kim](https://www.instagram.com/jin_252_) (Artist)
 - [Choo Heonsoo](https://www.instagram.com/hohenheim_plask) (3D Modelling)
 - [Eunsong Shin](https://www.instagram.com/comp._.silversssong/) (Sound Design)
 - [Long Hoang](https://github.com/loong/) (Engineering)

## Features

- 🎭 AI choreographic director with poetic, precise physical directions
- 🗣️ Natural voice synthesis using ElevenLabs with multilingual support
- 📷 Real-time camera analysis and continuous feedback
- 🎬 Multiple director options including pre-recorded and live AI responses
- 🌍 Bilingual instructions (English and Korean)
- 🎯 Body-focused choreographic guidance inspired by renowned directors

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

Test your API keys before running the application:

```bash
python test_api_keys.py
```

This will verify that both your OpenAI and ElevenLabs API keys are valid and working.

## Usage

### AI Theatre Director

```bash
python ai_director.py
```

The AI Director embodies a choreographic vision that sees only bodies in motion. It provides poetic, precise physical directions inspired by the spirits of Pina Bausch, Herzog, Scorsese, Ocean Vuong, and Barthes.

#### How It Works:

1. **Camera Detection** - Automatically scans and lets you select from available cameras
2. **Director Selection** - Choose from 4 director options:
   - Directors 1-3: Pre-recorded audio responses
   - Director 4: Live AI-generated instructions with voice synthesis
3. **Real-time Analysis** - Continuously analyzes your movement through the camera
4. **Voice Feedback** - Provides spoken directions in both English and Korean

#### Director Personality:

The AI director follows a specific ritual:
- Declares possession of your body upon detection
- Provides precise, poetic, and physical directions
- Focuses solely on body movement and positioning
- Delivers instructions with emotional undertones and spatial commands
- Concludes each direction with affirmation

#### Configuration Options:

- **Analysis Frequency**: Adjustable FPS for frame capture (default: 0.3)
- **Frames per Analysis**: Number of frames analyzed together (default: 2)
- **Camera Selection**: Choose from detected cameras
- **Director Type**: Switch between pre-recorded and live AI responses

### Example Session

```bash
# Activate virtual environment
source venv/bin/activate

# Run the AI Director
python ai_director.py

# Follow the prompts to:
# 1. Select your camera
# 2. Configure analysis settings
# 3. Choose director type during session
# 4. Receive real-time choreographic guidance
```
