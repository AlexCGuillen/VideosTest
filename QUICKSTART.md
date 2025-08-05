# Quick Start Guide 🚀

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/AlexCGuillen/VideosTest.git
cd VideosTest
```

2. **Install dependencies (optional but recommended):**
```bash
pip install -r requirements.txt
```

3. **Set up API key (optional):**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Basic Usage

### Option 1: Command Line (Recommended)
```bash
# Basic usage
python main.py your_movie.mp4

# With custom settings
python main.py movie.mp4 --output-dir ./tiktoks --duration 30 --title "My Movie"
```

### Option 2: Python Script
```python
from tiktok_generator import TikTokVideoGenerator
from config import Config

config = Config()
generator = TikTokVideoGenerator(config)

videos = generator.generate_videos("movie.mp4", "./output")
print(f"Created {len(videos)} TikTok videos!")
```

## Test the System

```bash
# Run system check
python test_setup.py

# Run quick demo
python quick_demo.py

# See usage examples
python examples.py
```

## Output

The system creates:
- Multiple MP4 files optimized for TikTok (1080x1920)
- AI-generated narration audio
- Suggested descriptions for posting
- Organized file structure

## Monetization Strategy

1. **Post Schedule**: Upload parts daily
2. **Hashtags**: Use relevant movie/genre tags
3. **Engagement**: Respond to comments quickly
4. **Series Format**: Clear part numbering
5. **Cliffhangers**: End with suspense

## Troubleshooting

- **Missing dependencies**: The system works with graceful fallbacks
- **No AI key**: Uses template narrations
- **Internet issues**: Creates placeholder audio files
- **FFmpeg missing**: Install from https://ffmpeg.org/

## File Structure

```
VideosTest/
├── main.py              # Main CLI application
├── config.py            # Configuration settings
├── tiktok_generator.py  # Core generator class
├── video_processor.py   # Video processing
├── ai_generator.py      # AI narration scripts
├── tts_generator.py     # Text-to-speech
├── utils.py             # Utility functions
├── test_setup.py        # System tests
├── quick_demo.py        # Quick demonstration
├── examples.py          # Usage examples
└── requirements.txt     # Dependencies
```

## Ready to Go! 🎬

You now have everything needed to transform movies into monetizable TikTok content!