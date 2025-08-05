#!/usr/bin/env python3
"""
Demo script for TikTok Video Generator

This script demonstrates the basic functionality with a mock video file.
"""

import os
import tempfile
from pathlib import Path

# Add current directory to path
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tiktok_generator import TikTokVideoGenerator
from config import Config

def create_demo_video():
    """Create a simple demo 'video' file for testing."""
    demo_dir = tempfile.mkdtemp()
    demo_video = os.path.join(demo_dir, "demo_movie.mp4")
    
    # Create a placeholder file
    with open(demo_video, 'w') as f:
        f.write("This is a demo video file for testing purposes.\n")
        f.write("In a real scenario, this would be an actual MP4 video file.\n")
    
    return demo_video

def main():
    """Run the demo."""
    print("🎬 TikTok Video Generator - Demo")
    print("=" * 50)
    
    # Create demo video file
    demo_video = create_demo_video()
    print(f"Created demo video: {demo_video}")
    
    # Initialize configuration
    config = Config()
    config.video.segment_duration = 15  # Shorter segments for demo
    
    # Initialize generator
    generator = TikTokVideoGenerator(config)
    
    # Create output directory
    output_dir = "./demo_output"
    
    try:
        print(f"\n🚀 Starting video generation...")
        print(f"Input: {demo_video}")
        print(f"Output: {output_dir}")
        
        # Generate videos
        output_files = generator.generate_videos(
            input_video=demo_video,
            output_dir=output_dir,
            video_title="Demo Movie"
        )
        
        # Generate description
        description = generator.generate_description("Demo Movie", len(output_files))
        
        print(f"\n✅ Demo completed successfully!")
        print(f"📁 Generated files in: {output_dir}")
        print(f"📱 Number of segments: {len(output_files)}")
        print(f"\n📝 Generated description:")
        print(f"   {description}")
        
        # Show what was created
        if os.path.exists(output_dir):
            print(f"\n📂 Contents of {output_dir}:")
            for file in sorted(os.listdir(output_dir)):
                file_path = os.path.join(output_dir, file)
                size = os.path.getsize(file_path)
                print(f"   {file} ({size} bytes)")
        
        print(f"\n💡 Note: This is a demo with placeholder files.")
        print(f"   Install dependencies for full video processing:")
        print(f"   pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return 1
    
    finally:
        # Cleanup demo video
        if os.path.exists(demo_video):
            os.unlink(demo_video)
            os.rmdir(os.path.dirname(demo_video))
    
    return 0

if __name__ == "__main__":
    exit(main())