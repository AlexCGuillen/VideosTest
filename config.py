"""Configuration settings for the TikTok video generator."""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class VideoConfig:
    """Configuration for video processing."""
    # TikTok optimal dimensions (vertical)
    width: int = 1080
    height: int = 1920
    fps: int = 30
    
    # Segment settings
    segment_duration: int = 30  # seconds
    overlap_duration: float = 0.5  # seconds of overlap between segments
    
    # Audio settings
    audio_bitrate: str = "128k"
    narration_volume: float = 0.8
    original_audio_volume: float = 0.3

@dataclass
class AIConfig:
    """Configuration for AI text generation."""
    openai_api_key: Optional[str] = None
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 150
    temperature: float = 0.7
    
    # Narration prompts
    narration_style: str = "engaging and dramatic"
    target_audience: str = "young adults interested in movies"

@dataclass
class TTSConfig:
    """Configuration for text-to-speech."""
    language: str = "en"
    slow: bool = False
    tld: str = "com"  # Top level domain for different accents

class Config:
    """Main configuration class."""
    def __init__(self):
        self.video = VideoConfig()
        self.ai = AIConfig()
        self.tts = TTSConfig()
        
        # Load environment variables
        self.ai.openai_api_key = os.getenv("OPENAI_API_KEY")
        
    def validate(self) -> bool:
        """Validate configuration."""
        if not self.ai.openai_api_key:
            print("Warning: OPENAI_API_KEY not set. AI narration will be limited.")
            return False
        return True