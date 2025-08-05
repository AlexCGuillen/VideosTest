"""AI text generation module for creating narration scripts."""

from typing import List, Optional
from config import AIConfig
import time

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

class AIScriptGenerator:
    """Generates narration scripts using AI."""
    
    def __init__(self, config: AIConfig):
        self.config = config
        if config.openai_api_key and HAS_OPENAI:
            openai.api_key = config.openai_api_key
        
    def generate_narration(self, video_context: str, segment_number: int, 
                          total_segments: int, timestamp: str) -> str:
        """Generate narration for a video segment."""
        if not self.config.openai_api_key or not HAS_OPENAI:
            return self._generate_fallback_narration(video_context, segment_number, timestamp)
        
        prompt = self._create_prompt(video_context, segment_number, total_segments, timestamp)
        
        try:
            response = openai.ChatCompletion.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": "You are a creative storyteller who creates engaging narrations for TikTok videos."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                n=1
            )
            
            narration = response.choices[0].message.content.strip()
            print(f"Generated AI narration for segment {segment_number}")
            return narration
            
        except Exception as e:
            print(f"Error generating AI narration: {e}")
            return self._generate_fallback_narration(video_context, segment_number, timestamp)
    
    def _create_prompt(self, video_context: str, segment_number: int, 
                      total_segments: int, timestamp: str) -> str:
        """Create a prompt for AI narration generation."""
        part_text = f"Part {segment_number} of {total_segments}"
        
        prompt = f"""
        Create an engaging and {self.config.narration_style} narration for a TikTok video segment.
        
        Video context: {video_context}
        Segment: {part_text} (timestamp: {timestamp})
        Target audience: {self.config.target_audience}
        
        Guidelines:
        - Keep it under 25 words for a 30-second clip
        - Make it dramatic and attention-grabbing
        - Use cliffhangers or questions to keep viewers engaged
        - Mention this is "{part_text}" if it's part of a series
        - Focus on the most exciting aspects of this segment
        - Use present tense and active voice
        
        Generate only the narration text, no additional formatting:
        """
        
        return prompt
    
    def _generate_fallback_narration(self, video_context: str, segment_number: int, 
                                   timestamp: str) -> str:
        """Generate a simple fallback narration when AI is not available."""
        templates = [
            f"Part {segment_number}: The story continues at {timestamp}...",
            f"What happens next in Part {segment_number}? Watch to find out!",
            f"Part {segment_number}: The tension builds at {timestamp}!",
            f"You won't believe what happens in Part {segment_number}!",
            f"Part {segment_number}: The plot thickens at {timestamp}...",
            f"Amazing scenes in Part {segment_number} starting at {timestamp}!",
            f"Part {segment_number}: The adventure continues!",
            f"Don't miss what happens in Part {segment_number}!",
            f"Part {segment_number}: Things get intense at {timestamp}!",
            f"The story gets better in Part {segment_number}!"
        ]
        
        # Simple rotation based on segment number
        template_index = (segment_number - 1) % len(templates)
        return templates[template_index]
    
    def generate_video_description(self, video_title: str, total_segments: int) -> str:
        """Generate a description for the video series."""
        if not self.config.openai_api_key or not HAS_OPENAI:
            return f"🎬 {video_title} - {total_segments} part series! Follow for more movie content! #movies #storytelling #viral"
        
        prompt = f"""
        Create a TikTok-style description for a video series about: {video_title}
        The series has {total_segments} parts.
        
        Make it:
        - Engaging and clickbait-style
        - Include relevant hashtags
        - Encourage following and engagement
        - Under 100 characters
        
        Generate only the description:
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": "You are a social media expert creating viral TikTok descriptions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=80,
                temperature=0.8,
                n=1
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating description: {e}")
            return f"🎬 {video_title} - {total_segments} part series! Follow for more! #movies #viral #storytelling"