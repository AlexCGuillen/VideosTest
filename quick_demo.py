#!/usr/bin/env python3
"""
Simple demo for TikTok Video Generator core functionality.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from ai_generator import AIScriptGenerator
from tts_generator import TextToSpeechGenerator

def demo_ai_generation():
    """Demo AI script generation."""
    print("🤖 AI Script Generation Demo")
    print("-" * 30)
    
    config = Config()
    ai_gen = AIScriptGenerator(config.ai)
    
    # Generate sample narrations
    movie_title = "Epic Adventure Movie"
    for i in range(3):
        narration = ai_gen.generate_narration(
            video_context=movie_title,
            segment_number=i+1,
            total_segments=5,
            timestamp=f"{i*30}:{(i*30)%60:02d}-{(i+1)*30}:{((i+1)*30)%60:02d}"
        )
        print(f"Part {i+1}: {narration}")
    
    # Generate description
    description = ai_gen.generate_video_description(movie_title, 5)
    print(f"\nDescription: {description}")

def demo_tts():
    """Demo text-to-speech functionality."""
    print("\n🔊 Text-to-Speech Demo")
    print("-" * 30)
    
    config = Config()
    tts_gen = TextToSpeechGenerator(config.tts)
    
    # Test TTS functionality
    success = tts_gen.test_tts()
    if success:
        print("✅ TTS system ready")
    else:
        print("❌ TTS system not available")
    
    # Generate sample audio
    sample_text = "Welcome to Part 1 of our amazing movie series!"
    try:
        audio_path = tts_gen.generate_speech(sample_text)
        print(f"Generated audio: {audio_path}")
        
        # Check if file exists
        if os.path.exists(audio_path):
            size = os.path.getsize(audio_path)
            print(f"File size: {size} bytes")
        
    except Exception as e:
        print(f"Error: {e}")

def demo_config():
    """Demo configuration system."""
    print("\n⚙️ Configuration Demo")
    print("-" * 30)
    
    config = Config()
    print(f"Video: {config.video.width}x{config.video.height}")
    print(f"Segment duration: {config.video.segment_duration}s")
    print(f"AI model: {config.ai.model}")
    print(f"TTS language: {config.tts.language}")
    
    valid = config.validate()
    print(f"Configuration valid: {'✅' if valid else '❌'}")

def main():
    """Run all demos."""
    print("🎬 TikTok Video Generator - Quick Demo")
    print("=" * 50)
    
    demo_config()
    demo_ai_generation()
    demo_tts()
    
    print("\n✨ Demo completed!")
    print("\nNext steps:")
    print("1. Install full dependencies: pip install -r requirements.txt")
    print("2. Set OpenAI API key in .env file (optional)")
    print("3. Run with real video: python main.py your_movie.mp4")
    
    return 0

if __name__ == "__main__":
    exit(main())