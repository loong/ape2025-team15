#!/usr/bin/env python3
"""
Test script to validate API keys for the Video Analysis Tool
"""

from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

def test_openai_key():
    """Test OpenAI API key"""
    print("\n🔍 Testing OpenAI API Key...")
    print("-" * 40)
    
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        return False
    
    print(f"✓ Key found: {key[:7]}...{key[-4:]}")
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        
        # Test with a simple request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'API key works'"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✓ API Response: {result}")
        print("✅ OpenAI API key is valid and working!")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API test failed: {e}")
        return False


def test_elevenlabs_key():
    """Test ElevenLabs API key"""
    print("\n🔍 Testing ElevenLabs API Key...")
    print("-" * 40)
    
    key = os.getenv("ELEVENLABS_API_KEY")
    if not key:
        print("❌ ELEVENLABS_API_KEY not found in environment variables")
        return False
    
    print(f"✓ Key found: {key[:8]}...{key[-4:]}")
    
    try:
        from elevenlabs import ElevenLabs
        
        # Initialize client with API key
        client = ElevenLabs(api_key=key)
        
        # Get available voices
        voices_response = client.voices.get_all()
        available_voices = voices_response.voices
        
        if available_voices:
            print(f"✓ Found {len(available_voices)} available voices:")
            for i, voice in enumerate(available_voices[:5]):  # Show first 5
                print(f"  - {voice.name} ({voice.voice_id})")
            if len(available_voices) > 5:
                print(f"  ... and {len(available_voices) - 5} more")
            print("✅ ElevenLabs API key is valid and working!")
            return True
        else:
            print("❌ No voices found - API key might be invalid")
            return False
            
    except Exception as e:
        print(f"❌ ElevenLabs API test failed: {e}")
        return False


def check_env_file():
    """Check if .env file exists and has the required keys"""
    print("\n📄 Checking .env file...")
    print("-" * 40)
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("\nCreate a .env file with the following content:")
        print("OPENAI_API_KEY=your_openai_api_key_here")
        print("ELEVENLABS_API_KEY=your_elevenlabs_api_key_here")
        return False
    
    print("✓ .env file found")
    
    # Check for required keys
    with open('.env', 'r') as f:
        content = f.read()
        
    has_openai = 'OPENAI_API_KEY' in content
    has_elevenlabs = 'ELEVENLABS_API_KEY' in content
    
    if has_openai:
        print("✓ OPENAI_API_KEY found in .env")
    else:
        print("❌ OPENAI_API_KEY not found in .env")
        
    if has_elevenlabs:
        print("✓ ELEVENLABS_API_KEY found in .env")
    else:
        print("❌ ELEVENLABS_API_KEY not found in .env")
    
    return has_openai and has_elevenlabs


def main():
    print("🔐 API Key Validation Tool")
    print("=" * 50)
    print("This tool will test your API keys for:")
    print("- OpenAI (GPT-4 Vision)")
    print("- ElevenLabs (Text-to-Speech)")
    
    # Check .env file
    env_ok = check_env_file()
    
    if not env_ok:
        print("\n❌ Please fix your .env file first!")
        sys.exit(1)
    
    # Test API keys
    openai_ok = test_openai_key()
    elevenlabs_ok = test_elevenlabs_key()
    
    # Summary
    print("\n📊 Summary")
    print("=" * 50)
    print(f"OpenAI API Key:     {'✅ Valid' if openai_ok else '❌ Invalid'}")
    print(f"ElevenLabs API Key: {'✅ Valid' if elevenlabs_ok else '❌ Invalid'}")
    
    if openai_ok and elevenlabs_ok:
        print("\n✅ All API keys are valid! You're ready to use the tools.")
        print("\nYou can now run:")
        print("- python video_analyzer.py")
        print("- python ai_director.py")
    else:
        print("\n❌ Some API keys are invalid. Please check and update them.")
        print("\nGet your API keys from:")
        print("- OpenAI: https://platform.openai.com/api-keys")
        print("- ElevenLabs: https://elevenlabs.io/")


if __name__ == "__main__":
    main() 