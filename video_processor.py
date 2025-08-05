"""Video processing module for TikTok video generation."""

import os
from typing import List, Tuple
import tempfile

try:
    from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
    HAS_MOVIEPY = True
except ImportError:
    HAS_MOVIEPY = False

from config import VideoConfig

class VideoProcessor:
    """Handles video processing operations."""
    
    def __init__(self, config: VideoConfig):
        self.config = config
        
    def load_video(self, video_path: str):
        """Load a video file."""
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        if not HAS_MOVIEPY:
            print("⚠️  MoviePy not available. Creating mock video object.")
            return MockVideoClip(video_path)
        
        try:
            video = VideoFileClip(video_path)
            print(f"Loaded video: {video_path}")
            print(f"Duration: {video.duration:.2f}s, Size: {video.size}")
            return video
        except Exception as e:
            raise Exception(f"Error loading video: {e}")
    
    def extract_segments(self, video) -> List[Tuple[float, float]]:
        """Extract segment timestamps from video."""
        segments = []
        
        if HAS_MOVIEPY:
            duration = video.duration
        else:
            duration = video.duration  # Mock object
            
        segment_duration = self.config.segment_duration
        overlap = self.config.overlap_duration
        
        start_time = 0
        while start_time < duration:
            end_time = min(start_time + segment_duration, duration)
            segments.append((start_time, end_time))
            start_time = end_time - overlap
            
        print(f"Extracted {len(segments)} segments from video")
        return segments
    
    def resize_for_tiktok(self, video):
        """Resize video to TikTok format (9:16 aspect ratio)."""
        if not HAS_MOVIEPY:
            print("⚠️  MoviePy not available. Returning original video.")
            return video
            
        target_width = self.config.width
        target_height = self.config.height
        
        # Calculate scaling to fit the video properly
        video_aspect = video.w / video.h
        target_aspect = target_width / target_height
        
        if video_aspect > target_aspect:
            # Video is wider, scale by height and crop width
            new_height = target_height
            new_width = int(video_aspect * new_height)
            resized = video.resize(height=new_height)
            # Center crop
            x_center = new_width // 2
            x1 = x_center - target_width // 2
            x2 = x1 + target_width
            resized = resized.crop(x1=x1, x2=x2)
        else:
            # Video is taller, scale by width and crop height
            new_width = target_width
            new_height = int(new_width / video_aspect)
            resized = video.resize(width=new_width)
            # Center crop
            y_center = new_height // 2
            y1 = y_center - target_height // 2
            y2 = y1 + target_height
            resized = resized.crop(y1=y1, y2=y2)
        
        return resized
    
    def create_segment(self, video, start_time: float, 
                      end_time: float, narration_audio_path: str = None):
        """Create a video segment with optional narration."""
        if not HAS_MOVIEPY:
            print(f"⚠️  MoviePy not available. Creating placeholder segment {start_time:.1f}s-{end_time:.1f}s")
            return MockVideoClip(f"segment_{start_time:.1f}_{end_time:.1f}")
        
        # Extract the segment
        segment = video.subclip(start_time, end_time)
        
        # Resize for TikTok
        segment = self.resize_for_tiktok(segment)
        
        # Add narration if provided and it's a real audio file
        if narration_audio_path and os.path.exists(narration_audio_path) and narration_audio_path.endswith('.mp3'):
            narration_audio = AudioFileClip(narration_audio_path)
            
            # Mix original audio (reduced volume) with narration
            original_audio = segment.audio.volumex(self.config.original_audio_volume)
            narration_audio = narration_audio.volumex(self.config.narration_volume)
            
            # Ensure narration doesn't exceed segment duration
            if narration_audio.duration > segment.duration:
                narration_audio = narration_audio.subclip(0, segment.duration)
            
            mixed_audio = CompositeAudioClip([original_audio, narration_audio])
            segment = segment.set_audio(mixed_audio)
        
        return segment
    
    def save_segment(self, segment, output_path: str) -> None:
        """Save a video segment to file."""
        if not HAS_MOVIEPY:
            print(f"⚠️  MoviePy not available. Creating placeholder file: {output_path}")
            # Create a placeholder file
            with open(output_path.replace('.mp4', '_placeholder.txt'), 'w') as f:
                f.write(f"Video segment placeholder: {segment.name if hasattr(segment, 'name') else 'segment'}")
            return
            
        try:
            segment.write_videofile(
                output_path,
                fps=self.config.fps,
                audio_bitrate=self.config.audio_bitrate,
                verbose=False,
                logger=None
            )
            print(f"Saved segment: {output_path}")
        except Exception as e:
            raise Exception(f"Error saving segment: {e}")
        finally:
            segment.close()

class MockVideoClip:
    """Mock video clip for testing without MoviePy."""
    
    def __init__(self, name):
        self.name = name
        self.duration = 120.0  # 2 minutes default
        self.w = 1920
        self.h = 1080
        self.size = (self.w, self.h)
        self.fps = 30
        
    def close(self):
        pass