#!/usr/bin/env python3
"""
TikTok Video Generator Launcher

Simple launcher that provides both GUI and CLI interfaces for the TikTok video generator.
Perfect for users who want an easy way to start the application.
"""

import sys
import os

def show_options():
    """Show available options to the user."""
    print("🎬 TikTok Video Generator")
    print("=" * 50)
    print()
    print("Choose how you want to use the application:")
    print()
    print("1. 🌐 Web GUI (Recommended - Works everywhere)")
    print("   Modern web interface that works in any browser")
    print()
    print("2. 🖱️  Desktop GUI (Requires tkinter)")
    print("   Native desktop interface for local use")
    print()
    print("3. 💻 Command Line Mode")
    print("   For advanced users who prefer terminal interface")
    print()
    print("4. 📚 Show Usage Examples")
    print("   See command line examples and API usage")
    print()
    print("5. 📖 Show Manual Upload Guide")
    print("   Step-by-step guide for uploading to TikTok")
    print()

def launch_web_gui():
    """Launch the web GUI interface."""
    try:
        print("🌐 Starting web interface...")
        from web_gui import TikTokWebGUI
        gui = TikTokWebGUI()
        gui.run()
        return True
    except ImportError as e:
        print("❌ Error: Could not start web interface")
        print(f"   Missing dependency: {e}")
        print("   Install Flask: pip install flask")
        return False
    except Exception as e:
        print(f"❌ Error starting web GUI: {e}")
        return False

def launch_gui():
    """Launch the desktop GUI interface."""
    try:
        print("🖱️  Starting desktop GUI interface...")
        from gui import TikTokGeneratorGUI
        app = TikTokGeneratorGUI()
        app.run()
        return True
    except ImportError as e:
        print("❌ Error: Could not start desktop GUI interface")
        if "tkinter" in str(e).lower():
            print("   tkinter is not available on this system")
            print("   Try the web interface instead (option 1)")
        else:
            print(f"   Missing dependency: {e}")
        return False
    except Exception as e:
        print(f"❌ Error starting desktop GUI: {e}")
        return False

def launch_cli():
    """Launch the command line interface."""
    print("💻 Command Line Mode")
    print("=" * 30)
    print()
    
    if len(sys.argv) > 1:
        # Arguments were passed, run directly
        from tiktok_generator import main
        main()
    else:
        # Interactive mode
        print("Enter the path to your video file:")
        video_path = input("Video file: ").strip()
        
        if not video_path or not os.path.exists(video_path):
            print("❌ Invalid video file path")
            return False
        
        print("\nEnter output directory (press Enter for './tiktok_videos'):")
        output_dir = input("Output directory: ").strip() or "./tiktok_videos"
        
        print("\nEnter video title (press Enter to use filename):")
        title = input("Title: ").strip() or None
        
        print("\nEnter segment duration in seconds (press Enter for 30):")
        try:
            duration = input("Duration: ").strip()
            duration = int(duration) if duration else 30
        except ValueError:
            duration = 30
        
        # Run with the provided parameters
        try:
            from tiktok_generator import TikTokVideoGenerator
            from config import Config
            
            config = Config()
            config.video.segment_duration = duration
            
            generator = TikTokVideoGenerator(config)
            output_files = generator.generate_videos(video_path, output_dir, title)
            
            print(f"\n✅ Successfully generated {len(output_files)} TikTok videos!")
            print(f"📁 Output directory: {output_dir}")
            
            # Show manual upload guide
            from tiktok_uploader import TikTokUploadGuide
            description = generator.generate_description(title or os.path.basename(video_path), len(output_files))
            TikTokUploadGuide.print_manual_upload_guide(output_files, description)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    return True

def show_examples():
    """Show usage examples."""
    print("📚 Usage Examples")
    print("=" * 30)
    print()
    print("Command Line Examples:")
    print()
    print("# Basic usage")
    print("python launcher.py movie.mp4")
    print()
    print("# With custom settings")
    print("python tiktok_generator.py movie.mp4 --output-dir ./my_tiktoks --duration 45 --title 'Epic Movie'")
    print()
    print("# Using the API")
    print("from tiktok_generator import TikTokVideoGenerator")
    print("from config import Config")
    print()
    print("config = Config()")
    print("config.video.segment_duration = 30")
    print("generator = TikTokVideoGenerator(config)")
    print("videos = generator.generate_videos('movie.mp4', './output')")
    print()
    print("# For GUI mode, just run:")
    print("python launcher.py")
    print("# And select option 1")
    print()

def show_upload_guide():
    """Show manual upload guide."""
    from tiktok_uploader import TikTokUploadGuide
    
    example_files = ["movie_part_001.mp4", "movie_part_002.mp4", "movie_part_003.mp4"]
    example_description = "Epic movie moments that will blow your mind! 🎬✨ Part 1 of 3 #fyp #movie #viral"
    
    TikTokUploadGuide.print_manual_upload_guide(example_files, example_description)

def main():
    """Main launcher function."""
    # If arguments are provided, assume CLI mode
    if len(sys.argv) > 1:
        # Check for special flags
        if sys.argv[1] in ['--web-gui', '-w']:
            launch_web_gui()
            return
        elif sys.argv[1] in ['--gui', '-g']:
            launch_gui()
            return
        elif sys.argv[1] in ['--help', '-h']:
            show_examples()
            return
        elif sys.argv[1] in ['--upload-guide', '-u']:
            show_upload_guide()
            return
        else:
            # Pass to CLI handler
            launch_cli()
            return
    
    # Interactive mode
    while True:
        show_options()
        
        try:
            choice = input("Enter your choice (1-5, or 'q' to quit): ").strip().lower()
            
            if choice in ['q', 'quit', 'exit']:
                print("👋 Goodbye!")
                break
            elif choice == '1':
                if launch_web_gui():
                    break
            elif choice == '2':
                if launch_gui():
                    break
            elif choice == '3':
                if launch_cli():
                    break
            elif choice == '4':
                show_examples()
                input("\nPress Enter to continue...")
            elif choice == '5':
                show_upload_guide()
                input("\nPress Enter to continue...")
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, 4, 5, or 'q'")
            
            print()  # Add spacing
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()