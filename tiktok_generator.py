"""Main TikTok video generator application."""

import os
import tempfile
import shutil
from pathlib import Path

try:
    import click
    HAS_CLICK = True
except ImportError:
    HAS_CLICK = False

try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False

from config import Config
from video_processor import VideoProcessor
from ai_generator import AIScriptGenerator
from tts_generator import TextToSpeechGenerator

class TikTokVideoGenerator:
    """Main class for generating TikTok videos from movies."""
    
    def __init__(self, config: Config):
        self.config = config
        self.video_processor = VideoProcessor(config.video)
        self.ai_generator = AIScriptGenerator(config.ai)
        self.tts_generator = TextToSpeechGenerator(config.tts)
    
    def generate_videos(self, input_video: str, output_dir: str, video_title: str = None) -> list:
        """Generate TikTok videos from input movie."""
        # Validate inputs
        if not os.path.exists(input_video):
            raise FileNotFoundError(f"Input video not found: {input_video}")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract video title if not provided
        if video_title is None:
            video_title = Path(input_video).stem
        
        print(f"Processing video: {video_title}")
        print(f"Input: {input_video}")
        print(f"Output directory: {output_dir}")
        
        try:
            # Load and process video
            video = self.video_processor.load_video(input_video)
            segments = self.video_processor.extract_segments(video)
            
            print(f"Will create {len(segments)} TikTok videos")
            
            # Generate narrations for all segments
            narrations = self._generate_narrations(video_title, segments, len(segments))
            
            # Generate TTS audio files
            tts_dir = tempfile.mkdtemp()
            audio_paths = self.tts_generator.generate_batch_speech(narrations, tts_dir)
            
            # Create video segments
            output_files = []
            for i, ((start_time, end_time), audio_path) in enumerate(zip(segments, audio_paths)):
                segment_num = i + 1
                output_filename = f"{video_title}_part_{segment_num:03d}.mp4"
                output_path = os.path.join(output_dir, output_filename)
                
                print(f"Creating segment {segment_num}/{len(segments)}: {start_time:.1f}s - {end_time:.1f}s")
                
                try:
                    segment = self.video_processor.create_segment(
                        video, start_time, end_time, audio_path
                    )
                    self.video_processor.save_segment(segment, output_path)
                    output_files.append(output_path)
                    
                except Exception as e:
                    print(f"Error creating segment {segment_num}: {e}")
                    continue
            
            # Cleanup
            if hasattr(video, 'close'):
                video.close()
            shutil.rmtree(tts_dir, ignore_errors=True)
            
            print(f"✅ Successfully created {len(output_files)} TikTok videos!")
            return output_files
            
        except Exception as e:
            print(f"❌ Error processing video: {e}")
            raise
    
    def _generate_narrations(self, video_title: str, segments: list, total_segments: int) -> list:
        """Generate narration texts for all segments."""
        narrations = []
        
        for i, (start_time, end_time) in enumerate(segments):
            segment_num = i + 1
            timestamp = f"{int(start_time//60)}:{int(start_time%60):02d}-{int(end_time//60)}:{int(end_time%60):02d}"
            
            narration = self.ai_generator.generate_narration(
                video_context=video_title,
                segment_number=segment_num,
                total_segments=total_segments,
                timestamp=timestamp
            )
            
            narrations.append(narration)
        
        return narrations
    
    def generate_description(self, video_title: str, total_segments: int) -> str:
        """Generate a description for the video series."""
        return self.ai_generator.generate_video_description(video_title, total_segments)

def simple_main():
    """Simple main function when click is not available."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python tiktok_generator.py <input_video> [output_dir] [title] [duration]")
        print("Example: python tiktok_generator.py movie.mp4 ./output 'My Movie' 30")
        return 1
    
    input_video = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './output'
    title = sys.argv[3] if len(sys.argv) > 3 else None
    duration = int(sys.argv[4]) if len(sys.argv) > 4 else 30
    
    # Load environment variables if available
    if HAS_DOTENV:
        load_dotenv()
    
    # Initialize configuration
    config = Config()
    config.video.segment_duration = duration
    
    # Validate configuration
    if not config.validate():
        print("⚠️  AI features may be limited without OpenAI API key")
        print("   Set OPENAI_API_KEY environment variable for full functionality")
    
    # Initialize generator
    generator = TikTokVideoGenerator(config)
    
    try:
        # Generate videos
        output_files = generator.generate_videos(input_video, output_dir, title)
        
        # Generate description
        description = generator.generate_description(title or Path(input_video).stem, len(output_files))
        
        print(f"\n🎉 Generation complete!")
        print(f"📁 Output directory: {output_dir}")
        print(f"📱 Generated {len(output_files)} TikTok videos")
        print(f"\n📝 Suggested description:")
        print(f"   {description}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if HAS_CLICK:
    @click.command()
    @click.argument('input_video', type=click.Path(exists=True))
    @click.option('--output-dir', '-o', default='./output', help='Output directory for generated videos')
    @click.option('--title', '-t', help='Video title (defaults to filename)')
    @click.option('--duration', '-d', default=30, help='Segment duration in seconds')
    @click.option('--config-file', help='Path to configuration file')
    def main(input_video, output_dir, title, duration, config_file):
        """Generate TikTok videos from a movie file."""
        
        # Load environment variables
        if HAS_DOTENV:
            load_dotenv()
        
        # Initialize configuration
        config = Config()
        config.video.segment_duration = duration
        
        # Validate configuration
        if not config.validate():
            print("⚠️  AI features may be limited without OpenAI API key")
            print("   Set OPENAI_API_KEY environment variable for full functionality")
        
        # Initialize generator
        generator = TikTokVideoGenerator(config)
        
        try:
            # Generate videos
            output_files = generator.generate_videos(input_video, output_dir, title)
            
            # Generate description
            description = generator.generate_description(title or Path(input_video).stem, len(output_files))
            
            print(f"\n🎉 Generation complete!")
            print(f"📁 Output directory: {output_dir}")
            print(f"📱 Generated {len(output_files)} TikTok videos")
            print(f"\n📝 Suggested description:")
            print(f"   {description}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1
        
        return 0
else:
    main = simple_main

if __name__ == '__main__':
    if HAS_CLICK:
        main()
    else:
        exit(simple_main())