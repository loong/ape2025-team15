#!/bin/bash

echo "🚀 Setting up Video Analysis Tool"
echo "================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  No .env file found!"
    echo "📝 Creating .env file..."
    echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
    echo ""
    echo "👉 Please edit .env and add your OpenAI API key"
    echo "   You can get one from: https://platform.openai.com/api-keys"
else
    echo "✅ .env file found"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "To run the video analyzer:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Make sure your OpenAI API key is set in .env"
echo "  3. Run: python video_analyzer.py"
echo ""
echo "Happy analyzing! 🎥" 