#!/usr/bin/env python3
"""
Example usage script for TikTok Video Generator

This script shows different ways to use the TikTok video generator.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tiktok_generator import TikTokVideoGenerator
from config import Config

def example_basic_usage():
    """Example 1: Basic usage with default settings."""
    print("📝 Example 1: Basic Usage")
    print("-" * 40)
    
    # Initialize with default configuration
    config = Config()
    generator = TikTokVideoGenerator(config)
    
    # Example parameters
    input_video = "my_movie.mp4"  # Your video file
    output_dir = "./tiktok_videos"
    
    print("Code:")
    print(f"""
from tiktok_generator import TikTokVideoGenerator
from config import Config

config = Config()
generator = TikTokVideoGenerator(config)

output_files = generator.generate_videos(
    input_video="{input_video}",
    output_dir="{output_dir}"
)

print(f"Generated {{len(output_files)}} TikTok videos!")
""")

def example_custom_settings():
    """Example 2: Custom settings."""
    print("\n📝 Example 2: Custom Settings")
    print("-" * 40)
    
    print("Code:")
    print("""
from tiktok_generator import TikTokVideoGenerator
from config import Config

# Initialize configuration
config = Config()

# Customize video settings
config.video.segment_duration = 45  # 45-second segments
config.video.width = 720  # Lower resolution
config.video.height = 1280
config.video.narration_volume = 0.9  # Louder narration

# Customize AI settings
config.ai.narration_style = "dramatic and mysterious"
config.ai.target_audience = "horror movie fans"

# Initialize generator
generator = TikTokVideoGenerator(config)

# Generate videos
output_files = generator.generate_videos(
    input_video="horror_movie.mp4",
    output_dir="./horror_tiktoks",
    video_title="Scary Movie Collection"
)

# Generate description
description = generator.generate_description("Scary Movie Collection", len(output_files))
print(f"Suggested description: {description}")
""")

def example_cli_usage():
    """Example 3: Command-line usage."""
    print("\n📝 Example 3: Command-Line Usage")
    print("-" * 40)
    
    print("Basic command:")
    print("python main.py movie.mp4")
    print()
    print("With custom options:")
    print("python main.py movie.mp4 --output-dir ./my_tiktoks --duration 20 --title 'Epic Movie'")
    print()
    print("All options:")
    print("python main.py --help")

def example_batch_processing():
    """Example 4: Batch processing multiple movies."""
    print("\n📝 Example 4: Batch Processing")
    print("-" * 40)
    
    print("Code:")
    print("""
import os
from pathlib import Path
from tiktok_generator import TikTokVideoGenerator
from config import Config

def process_movie_folder(input_folder, output_base_folder):
    config = Config()
    generator = TikTokVideoGenerator(config)
    
    # Find all video files
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    video_files = []
    
    for ext in video_extensions:
        video_files.extend(Path(input_folder).glob(f'*{ext}'))
    
    for video_file in video_files:
        movie_name = video_file.stem
        output_dir = os.path.join(output_base_folder, movie_name)
        
        print(f"Processing: {movie_name}")
        
        try:
            output_files = generator.generate_videos(
                input_video=str(video_file),
                output_dir=output_dir,
                video_title=movie_name
            )
            print(f"✅ Created {len(output_files)} videos for {movie_name}")
            
        except Exception as e:
            print(f"❌ Error processing {movie_name}: {e}")

# Usage
process_movie_folder("./movies", "./all_tiktok_videos")
""")

def example_monetization_tips():
    """Example 5: Monetization best practices."""
    print("\n💰 Monetization Tips")
    print("-" * 40)
    
    tips = [
        "Use engaging titles with cliffhangers",
        "Post consistently (daily if possible)",
        "Use trending hashtags related to your movie genre",
        "Engage with comments to boost algorithm visibility",
        "Create series with clear part numbers (Part 1, Part 2, etc.)",
        "Hook viewers in the first 3 seconds",
        "End with call-to-action ('Follow for Part X!')",
        "Cross-promote on other social platforms",
        "Collaborate with other creators",
        "Track analytics to optimize posting times"
    ]
    
    for i, tip in enumerate(tips, 1):
        print(f"{i:2d}. {tip}")

def main():
    """Run all examples."""
    print("🎬 TikTok Video Generator - Usage Examples")
    print("=" * 60)
    
    example_basic_usage()
    example_custom_settings()
    example_cli_usage()
    example_batch_processing()
    example_monetization_tips()
    
    print(f"\n🚀 Ready to start creating TikTok videos!")
    print(f"📚 See README.md for detailed installation instructions")
    print(f"🧪 Run quick_demo.py to test the system")

if __name__ == "__main__":
    main()