# TikTok Video Generator 🎬➡️📱

Transform movies into AI-narrated short videos optimized for TikTok posting and monetization!

## Features ✨

### 🎥 Core Video Processing
- **Smart Video Processing**: Automatically cuts movies into TikTok-optimized segments (9:16 aspect ratio)
- **AI Narration**: Generates engaging scripts using OpenAI GPT
- **Text-to-Speech**: Converts AI scripts to natural-sounding narration
- **TikTok Ready**: Outputs videos in perfect TikTok format (1080x1920, 30fps)
- **Audio Mixing**: Balances original movie audio with AI narration
- **Batch Processing**: Create multiple parts from a single movie

### 🖱️ User-Friendly Interface
- **Simple GUI**: Easy-to-use graphical interface for non-technical users
- **Command Line**: Advanced CLI for power users and automation
- **Smart Launcher**: Interactive menu to choose your preferred interface

### 🚀 TikTok Upload Integration
- **Automated Upload**: Experimental browser automation for direct TikTok uploads
- **Manual Upload Guide**: Step-by-step instructions for manual uploading
- **Upload Checklist**: Automatically generated checklist with descriptions and hashtags
- **Monetization Tips**: Built-in guidance for maximum engagement and revenue

### ⚙️ Advanced Configuration
- **Customizable Settings**: Adjust segment duration, narration style, video quality
- **API Integration**: OpenAI GPT for dynamic content generation
- **Graceful Fallbacks**: Works even with missing dependencies

## Quick Start 🚀

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/AlexCGuillen/VideosTest.git
cd VideosTest

# Install dependencies
pip install -r requirements.txt

# Optional: Install Selenium for automated uploads
pip install selenium
```

### 2. Setup API Key (Optional but Recommended)

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Choose Your Interface

#### 🖱️ Easy GUI Mode (Recommended for Beginners)
```bash
# Launch the simple interface
python launcher.py
# Select option 1 for GUI mode
```

The GUI provides a user-friendly interface where you can:
- Browse and select your input video file
- Choose output directory
- Adjust settings with sliders and checkboxes
- Monitor progress in real-time
- Optionally enable automatic TikTok uploads

#### 💻 Command Line Mode (Advanced Users)
```bash
# Basic usage
python main.py movie.mp4

# Advanced usage with custom settings
python main.py movie.mp4 --output-dir ./tiktok_videos --duration 30 --title "Amazing Movie"

# Interactive CLI mode
python launcher.py
# Select option 2 for CLI mode
```

#### 🚀 Quick Test
```bash
# Run demo to test your setup
python quick_demo.py

# Try the new UI features demo
python ui_demo.py
```

### 🎯 Simple Start (New Users)

If you're new to coding or just want the easiest way to get started:

```bash
# Download and install
git clone https://github.com/AlexCGuillen/VideosTest.git
cd VideosTest
pip install -r requirements.txt

# Launch the interactive interface
python launcher.py
```

This will show you a menu to choose between:
- **Web GUI** (works in any browser)
- **Desktop GUI** (native desktop app) 
- **Command Line** (for advanced users)
- **Usage Examples** and **Upload Guide**

## TikTok Upload Methods 📤

Once your videos are generated, you have several options for uploading to TikTok:

### 🤖 Automated Upload (Experimental)

Enable automated uploads directly through the application:

```bash
# GUI Mode: Check "Automatically upload to TikTok" option
python launcher.py

# Or programmatically:
from tiktok_uploader import TikTokUploader
uploader = TikTokUploader()
uploader.upload_video("video.mp4", "Description #fyp #viral")
```

**Features:**
- Browser automation using Selenium
- Batch upload multiple videos
- Automatic descriptions and hashtags
- Persistent login sessions

**Requirements:**
- Selenium: `pip install selenium`
- Chrome browser installed
- Manual login on first use

### 📱 Manual Upload (Recommended)

For maximum reliability and control:

1. **Generate videos** using the GUI or CLI
2. **Transfer to phone** via cloud storage, email, or USB
3. **Follow the checklist** automatically created in your output folder
4. **Upload to TikTok** using the mobile app

The generator creates an `UPLOAD_CHECKLIST.txt` with:
- ✅ Video file list
- ✅ Suggested descriptions and hashtags
- ✅ Step-by-step upload instructions
- ✅ Monetization tips and strategies

### 📖 Complete Upload Guide

See [UPLOAD_GUIDE.md](UPLOAD_GUIDE.md) for comprehensive instructions including:
- Detailed setup for automated uploads
- Manual upload best practices
- Troubleshooting common issues
- Monetization strategies
- TikTok API status and alternatives

## Usage Examples 📖

### Basic Video Processing
```bash
# Convert a movie into 30-second TikTok segments
python main.py "/path/to/movie.mp4"
```

### Customized Processing
```bash
# Custom segment duration and output directory
python main.py movie.mp4 --output-dir ./my_tiktoks --duration 45 --title "Epic Adventure"
```

### Using as Python Module
```python
from tiktok_generator import TikTokVideoGenerator
from config import Config

# Initialize
config = Config()
generator = TikTokVideoGenerator(config)

# Generate videos
output_files = generator.generate_videos(
    input_video="movie.mp4",
    output_dir="./output",
    video_title="My Movie"
)

print(f"Created {len(output_files)} TikTok videos!")
```

## Configuration ⚙️

Edit `config.py` to customize:

- **Video Settings**: Resolution, FPS, segment duration
- **AI Settings**: Model, prompts, narration style
- **Audio Settings**: Volume levels, bitrate

## Requirements 📋

### System Requirements
- Python 3.7+
- FFmpeg (for video processing)
- Internet connection (for TTS and AI)
- At least 1GB free disk space

### Python Dependencies
- moviepy (video processing)
- openai (AI text generation)
- gtts (text-to-speech)
- click (CLI interface)

## File Structure 📁

```
VideosTest/
├── main.py                 # Main entry point
├── tiktok_generator.py     # Core generator class
├── video_processor.py      # Video processing logic
├── ai_generator.py         # AI script generation
├── tts_generator.py        # Text-to-speech conversion
├── config.py              # Configuration settings
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

## Output Format 📱

Generated videos are optimized for TikTok:
- **Resolution**: 1080x1920 (9:16 aspect ratio)
- **Duration**: 15-60 seconds per segment
- **Format**: MP4 with H.264 encoding
- **Audio**: Mixed original audio + AI narration
- **Naming**: `MovieTitle_part_001.mp4`, `MovieTitle_part_002.mp4`, etc.

## Monetization Tips 💰

1. **Consistent Posting**: Upload parts regularly to build audience
2. **Engaging Titles**: Use the generated descriptions as templates
3. **Trending Hashtags**: Include relevant movie and genre hashtags
4. **Call-to-Action**: Encourage follows for next parts
5. **Series Format**: Number your parts clearly (Part 1, Part 2, etc.)

## Troubleshooting 🔧

### Common Issues

**FFmpeg not found**
```bash
# Install FFmpeg
# Windows: Download from https://ffmpeg.org/download.html
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
```

**OpenAI API Errors**
- Check your API key in `.env`
- Ensure you have credits in your OpenAI account
- Fallback narration will be used if API fails

**Memory Issues**
- Process shorter segments (reduce `segment_duration`)
- Close other applications
- Use lower resolution movies as input

### System Check
```bash
python -c "from utils import print_system_status; print_system_status()"
```

## License 📄

This project is open source. Feel free to modify and distribute according to your needs.

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support 💬

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the configuration options

---

**Happy TikTok creating! 🎬✨**
