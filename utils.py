"""Utility functions for the TikTok video generator."""

import os
import time
from pathlib import Path
from typing import List, Dict

def format_duration(seconds: float) -> str:
    """Format duration in seconds to MM:SS format."""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes}:{seconds:02d}"

def get_video_info(video_path: str) -> Dict:
    """Get basic information about a video file."""
    try:
        from moviepy.editor import VideoFileClip
        with VideoFileClip(video_path) as video:
            return {
                'duration': video.duration,
                'fps': video.fps,
                'size': video.size,
                'audio': video.audio is not None
            }
    except Exception as e:
        return {'error': str(e)}

def sanitize_filename(filename: str) -> str:
    """Sanitize a string to be used as a filename."""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip()

def create_output_structure(base_dir: str, video_title: str) -> Dict[str, str]:
    """Create organized output directory structure."""
    safe_title = sanitize_filename(video_title)
    
    structure = {
        'base': base_dir,
        'videos': os.path.join(base_dir, safe_title, 'videos'),
        'audio': os.path.join(base_dir, safe_title, 'audio'),
        'scripts': os.path.join(base_dir, safe_title, 'scripts'),
        'thumbnails': os.path.join(base_dir, safe_title, 'thumbnails')
    }
    
    for path in structure.values():
        os.makedirs(path, exist_ok=True)
    
    return structure

def estimate_processing_time(video_duration: float, segment_duration: int) -> float:
    """Estimate processing time based on video duration."""
    num_segments = video_duration / segment_duration
    # Rough estimate: 2-3 seconds per second of video
    return video_duration * 2.5

def validate_input_formats(file_path: str) -> bool:
    """Validate if the input file format is supported."""
    supported_formats = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}
    file_extension = Path(file_path).suffix.lower()
    return file_extension in supported_formats

def check_system_requirements() -> Dict[str, bool]:
    """Check if system requirements are met."""
    requirements = {
        'ffmpeg': False,
        'internet': False,
        'disk_space': False
    }
    
    # Check FFmpeg
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        requirements['ffmpeg'] = result.returncode == 0
    except:
        pass
    
    # Check internet connectivity (for TTS)
    try:
        import requests
        response = requests.get('https://google.com', timeout=5)
        requirements['internet'] = response.status_code == 200
    except:
        pass
    
    # Check disk space (simplified)
    try:
        import shutil
        free_space_gb = shutil.disk_usage('.').free / (1024**3)
        requirements['disk_space'] = free_space_gb > 1  # At least 1GB free
    except:
        pass
    
    return requirements

def print_system_status():
    """Print system requirements status."""
    print("System Requirements Check:")
    requirements = check_system_requirements()
    
    for req, status in requirements.items():
        status_symbol = "✅" if status else "❌"
        req_name = req.replace('_', ' ').title()
        print(f"  {status_symbol} {req_name}")
    
    if not all(requirements.values()):
        print("\n⚠️  Some requirements are not met. This may affect functionality.")
        if not requirements['ffmpeg']:
            print("   Install FFmpeg: https://ffmpeg.org/download.html")
        if not requirements['internet']:
            print("   Internet connection required for text-to-speech")
        if not requirements['disk_space']:
            print("   Ensure at least 1GB free disk space")
    else:
        print("\n✅ All requirements met!")

class ProgressTracker:
    """Simple progress tracker for long operations."""
    
    def __init__(self, total_steps: int):
        self.total_steps = total_steps
        self.current_step = 0
        self.start_time = time.time()
    
    def update(self, step_name: str = None):
        """Update progress."""
        self.current_step += 1
        progress = (self.current_step / self.total_steps) * 100
        elapsed = time.time() - self.start_time
        
        print(f"Progress: {progress:.1f}% ({self.current_step}/{self.total_steps})")
        if step_name:
            print(f"Current: {step_name}")
        if self.current_step > 0:
            eta = (elapsed / self.current_step) * (self.total_steps - self.current_step)
            print(f"ETA: {eta:.1f}s")
        print("─" * 40)