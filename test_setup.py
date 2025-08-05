#!/usr/bin/env python3
"""
Test script for the TikTok Video Generator

Run this to test basic functionality without processing a full video.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from ai_generator import AIScriptGenerator
from tts_generator import TextToSpeechGenerator
from utils import print_system_status, check_system_requirements

def test_configuration():
    """Test configuration loading."""
    print("🔧 Testing Configuration...")
    try:
        config = Config()
        print(f"✅ Config loaded successfully")
        print(f"   Video: {config.video.width}x{config.video.height}, {config.video.segment_duration}s segments")
        print(f"   AI Model: {config.ai.model}")
        print(f"   TTS Language: {config.tts.language}")
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_ai_generation():
    """Test AI narration generation."""
    print("\n🤖 Testing AI Generation...")
    try:
        config = Config()
        ai_gen = AIScriptGenerator(config.ai)
        
        narration = ai_gen.generate_narration(
            video_context="Test Movie",
            segment_number=1,
            total_segments=5,
            timestamp="0:00-0:30"
        )
        
        print(f"✅ AI generation successful")
        print(f"   Generated: '{narration}'")
        return True
    except Exception as e:
        print(f"❌ AI generation test failed: {e}")
        return False

def test_tts():
    """Test text-to-speech functionality."""
    print("\n🔊 Testing Text-to-Speech...")
    try:
        config = Config()
        tts_gen = TextToSpeechGenerator(config.tts)
        
        success = tts_gen.test_tts()
        if success:
            print("✅ TTS test successful")
        else:
            print("❌ TTS test failed")
        
        return success
    except Exception as e:
        print(f"❌ TTS test failed: {e}")
        return False

def test_imports():
    """Test all required imports."""
    print("\n📦 Testing Imports...")
    imports = {
        'moviepy': 'moviepy.editor',
        'openai': 'openai',
        'gtts': 'gtts',
        'click': 'click',
        'dotenv': 'dotenv'
    }
    
    results = {}
    for name, module in imports.items():
        try:
            __import__(module)
            results[name] = True
            print(f"✅ {name}")
        except ImportError as e:
            results[name] = False
            print(f"❌ {name}: {e}")
    
    return all(results.values())

def main():
    """Run all tests."""
    print("🧪 TikTok Video Generator - Test Suite")
    print("=" * 50)
    
    # System requirements check
    print_system_status()
    print()
    
    # Run tests
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("AI Generation", test_ai_generation),
        ("Text-to-Speech", test_tts)
    ]
    
    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to generate TikTok videos.")
    else:
        print("⚠️  Some tests failed. Check the requirements and configuration.")
        print("\nNext steps:")
        if not results.get("Imports", True):
            print("   1. Install dependencies: pip install -r requirements.txt")
        if not results.get("Text-to-Speech", True):
            print("   2. Check internet connection for TTS")
        if not results.get("AI Generation", True):
            print("   3. Set OPENAI_API_KEY in .env file (optional)")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())