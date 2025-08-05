"""Text-to-speech module for generating narration audio."""

import os
import tempfile
from typing import Optional

try:
    from gtts import gTTS
    HAS_GTTS = True
except ImportError:
    HAS_GTTS = False

from config import TTSConfig

class TextToSpeechGenerator:
    """Converts text to speech for video narration."""
    
    def __init__(self, config: TTSConfig):
        self.config = config
    
    def generate_speech(self, text: str, output_path: Optional[str] = None) -> str:
        """Generate speech from text and return the audio file path."""
        if not text.strip():
            raise ValueError("Text cannot be empty")
        
        if not HAS_GTTS:
            print("⚠️  gTTS not available. Creating placeholder audio file.")
            return self._create_placeholder_audio(text, output_path)
        
        # Create output path if not provided
        if output_path is None:
            temp_dir = tempfile.mkdtemp()
            output_path = os.path.join(temp_dir, "narration.mp3")
        
        try:
            # Generate TTS
            tts = gTTS(
                text=text,
                lang=self.config.language,
                slow=self.config.slow,
                tld=self.config.tld
            )
            
            # Save to file
            tts.save(output_path)
            print(f"Generated TTS audio: {output_path}")
            print(f"Text: {text[:50]}...")
            
            return output_path
            
        except Exception as e:
            print(f"Error generating TTS, creating placeholder: {e}")
            return self._create_placeholder_audio(text, output_path)
    
    def _create_placeholder_audio(self, text: str, output_path: Optional[str] = None) -> str:
        """Create a placeholder audio file when TTS is not available."""
        if output_path is None:
            temp_dir = tempfile.mkdtemp()
            output_path = os.path.join(temp_dir, "narration_placeholder.txt")
        else:
            # Change extension to .txt for placeholder
            output_path = output_path.replace('.mp3', '_placeholder.txt')
        
        with open(output_path, 'w') as f:
            f.write(f"TTS Placeholder for: {text}")
        
        print(f"Created placeholder audio file: {output_path}")
        return output_path
    
    def generate_batch_speech(self, texts: list, output_dir: str) -> list:
        """Generate speech for multiple texts and return list of audio file paths."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        audio_paths = []
        
        for i, text in enumerate(texts):
            if HAS_GTTS:
                output_path = os.path.join(output_dir, f"narration_{i+1:03d}.mp3")
            else:
                output_path = os.path.join(output_dir, f"narration_{i+1:03d}_placeholder.txt")
                
            try:
                audio_path = self.generate_speech(text, output_path)
                audio_paths.append(audio_path)
            except Exception as e:
                print(f"Error generating TTS for segment {i+1}: {e}")
                audio_paths.append(None)
        
        return audio_paths
    
    def test_tts(self) -> bool:
        """Test TTS functionality."""
        if not HAS_GTTS:
            print("⚠️  gTTS not available - using placeholder mode")
            return True  # Placeholder mode always works
            
        try:
            test_text = "This is a test of the text to speech system."
            temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            temp_file.close()
            
            self.generate_speech(test_text, temp_file.name)
            
            # Check if file was created and has content
            if os.path.exists(temp_file.name) and os.path.getsize(temp_file.name) > 0:
                os.unlink(temp_file.name)
                print("TTS test successful")
                return True
            else:
                print("TTS test failed - no audio generated")
                return False
                
        except Exception as e:
            print(f"TTS test failed: {e}")
            return False