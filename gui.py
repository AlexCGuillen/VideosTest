#!/usr/bin/env python3
"""
Simple GUI interface for TikTok Video Generator

A user-friendly graphical interface that allows non-technical users to easily
convert movies into TikTok videos without needing to use command line.
"""

import os
import threading
from pathlib import Path
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import queue

try:
    from tiktok_generator import TikTokVideoGenerator
    from config import Config
    from tiktok_uploader import TikTokUploader
    HAS_GENERATOR = True
except ImportError:
    HAS_GENERATOR = False

class TikTokGeneratorGUI:
    """Simple GUI for TikTok video generation."""
    
    def __init__(self):
        self.root = Tk()
        self.root.title("TikTok Video Generator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configuration
        self.config = Config() if HAS_GENERATOR else None
        self.generator = None
        self.uploader = None
        
        # GUI state
        self.input_video_path = StringVar()
        self.output_dir_path = StringVar(value="./tiktok_videos")
        self.video_title = StringVar()
        self.segment_duration = IntVar(value=30)
        self.auto_upload = BooleanVar(value=False)
        
        # Progress tracking
        self.progress_queue = queue.Queue()
        self.is_processing = False
        
        self.setup_ui()
        self.check_dependencies()
        
    def setup_ui(self):
        """Set up the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(W, E, N, S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="TikTok Video Generator", 
                               font=("Arial", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input video selection
        ttk.Label(main_frame, text="Input Video:").grid(row=1, column=0, sticky=W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_video_path, width=50).grid(
            row=1, column=1, sticky=(W, E), padx=(10, 5), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_input_video).grid(
            row=1, column=2, pady=5)
        
        # Output directory selection
        ttk.Label(main_frame, text="Output Directory:").grid(row=2, column=0, sticky=W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_dir_path, width=50).grid(
            row=2, column=1, sticky=(W, E), padx=(10, 5), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output_dir).grid(
            row=2, column=2, pady=5)
        
        # Video title
        ttk.Label(main_frame, text="Video Title (optional):").grid(row=3, column=0, sticky=W, pady=5)
        ttk.Entry(main_frame, textvariable=self.video_title, width=50).grid(
            row=3, column=1, sticky=(W, E), padx=(10, 5), pady=5)
        
        # Segment duration
        ttk.Label(main_frame, text="Segment Duration (seconds):").grid(row=4, column=0, sticky=W, pady=5)
        duration_frame = ttk.Frame(main_frame)
        duration_frame.grid(row=4, column=1, sticky=W, padx=(10, 5), pady=5)
        ttk.Scale(duration_frame, from_=15, to=60, variable=self.segment_duration, 
                 orient=HORIZONTAL, length=200).pack(side=LEFT)
        ttk.Label(duration_frame, textvariable=self.segment_duration).pack(side=LEFT, padx=(10, 0))
        
        # Auto upload option
        ttk.Checkbutton(main_frame, text="Automatically upload to TikTok (experimental)", 
                       variable=self.auto_upload).grid(row=5, column=0, columnspan=2, sticky=W, pady=10)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        self.generate_button = ttk.Button(button_frame, text="Generate TikTok Videos", 
                                         command=self.start_generation, style="Accent.TButton")
        self.generate_button.pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Open Output Folder", 
                  command=self.open_output_folder).pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Settings", 
                  command=self.open_settings).pack(side=LEFT)
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=7, column=0, columnspan=3, sticky=(W, E, N, S), pady=(20, 0))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=0, column=0, sticky=(W, E), pady=(0, 10))
        
        # Text output
        text_frame = ttk.Frame(progress_frame)
        text_frame.grid(row=1, column=0, sticky=(W, E, N, S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.output_text = Text(text_frame, height=15, wrap=WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=VERTICAL, command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        self.output_text.grid(row=0, column=0, sticky=(W, E, N, S))
        scrollbar.grid(row=0, column=1, sticky=(N, S))
        
        # Configure row weights for expansion
        main_frame.rowconfigure(7, weight=1)
        progress_frame.rowconfigure(1, weight=1)
        
    def check_dependencies(self):
        """Check if required dependencies are available."""
        if not HAS_GENERATOR:
            self.log_message("⚠️ Warning: Some dependencies are missing.")
            self.log_message("   Please install requirements: pip install -r requirements.txt")
            self.generate_button.config(state="disabled")
        else:
            self.log_message("✅ TikTok Video Generator ready!")
            if not self.config.validate():
                self.log_message("⚠️ Warning: OpenAI API key not configured.")
                self.log_message("   AI features will be limited. Set OPENAI_API_KEY for full functionality.")
    
    def browse_input_video(self):
        """Browse for input video file."""
        filetypes = [
            ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv"),
            ("MP4 files", "*.mp4"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(
            title="Select Input Video",
            filetypes=filetypes
        )
        if filename:
            self.input_video_path.set(filename)
            # Auto-set title from filename if not already set
            if not self.video_title.get():
                self.video_title.set(Path(filename).stem)
    
    def browse_output_dir(self):
        """Browse for output directory."""
        dirname = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.output_dir_path.get()
        )
        if dirname:
            self.output_dir_path.set(dirname)
    
    def open_output_folder(self):
        """Open the output folder in file explorer."""
        output_dir = self.output_dir_path.get()
        if os.path.exists(output_dir):
            # Platform-specific folder opening
            import subprocess
            import sys
            if sys.platform == "win32":
                os.startfile(output_dir)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", output_dir])
            else:
                subprocess.Popen(["xdg-open", output_dir])
        else:
            messagebox.showwarning("Warning", f"Output directory does not exist: {output_dir}")
    
    def open_settings(self):
        """Open settings dialog."""
        SettingsDialog(self.root, self.config)
    
    def log_message(self, message):
        """Add a message to the output text area."""
        self.output_text.insert(END, message + "\n")
        self.output_text.see(END)
        self.root.update_idletasks()
    
    def start_generation(self):
        """Start video generation in a separate thread."""
        if self.is_processing:
            return
            
        # Validate inputs
        if not self.input_video_path.get():
            messagebox.showerror("Error", "Please select an input video file.")
            return
            
        if not os.path.exists(self.input_video_path.get()):
            messagebox.showerror("Error", "Input video file does not exist.")
            return
            
        if not HAS_GENERATOR:
            messagebox.showerror("Error", "Generator dependencies are missing. Please install requirements.")
            return
        
        # Start processing
        self.is_processing = True
        self.generate_button.config(state="disabled", text="Processing...")
        self.progress_bar.start()
        
        # Clear output
        self.output_text.delete(1.0, END)
        
        # Start generation thread
        thread = threading.Thread(target=self.generate_videos_thread)
        thread.daemon = True
        thread.start()
        
        # Start checking for progress updates
        self.check_progress_queue()
    
    def generate_videos_thread(self):
        """Thread function for video generation."""
        try:
            # Update config with GUI values
            self.config.video.segment_duration = self.segment_duration.get()
            
            # Initialize generator
            self.generator = TikTokVideoGenerator(self.config)
            
            # Log start
            self.progress_queue.put(("log", f"🎬 Starting video generation..."))
            self.progress_queue.put(("log", f"Input: {self.input_video_path.get()}"))
            self.progress_queue.put(("log", f"Output: {self.output_dir_path.get()}"))
            self.progress_queue.put(("log", f"Segment duration: {self.segment_duration.get()}s"))
            
            # Generate videos
            output_files = self.generator.generate_videos(
                input_video=self.input_video_path.get(),
                output_dir=self.output_dir_path.get(),
                video_title=self.video_title.get() or None
            )
            
            self.progress_queue.put(("log", f"✅ Successfully generated {len(output_files)} videos!"))
            
            # Generate description
            title = self.video_title.get() or Path(self.input_video_path.get()).stem
            description = self.generator.generate_description(title, len(output_files))
            self.progress_queue.put(("log", f"\n📝 Suggested description:\n{description}"))
            
            # Auto-upload if enabled
            if self.auto_upload.get():
                self.progress_queue.put(("log", "\n🚀 Starting automatic upload..."))
                try:
                    from tiktok_uploader import TikTokUploader
                    self.uploader = TikTokUploader()
                    
                    for i, video_file in enumerate(output_files):
                        self.progress_queue.put(("log", f"Uploading video {i+1}/{len(output_files)}..."))
                        upload_result = self.uploader.upload_video(video_file, description)
                        if upload_result:
                            self.progress_queue.put(("log", f"✅ Uploaded: {Path(video_file).name}"))
                        else:
                            self.progress_queue.put(("log", f"❌ Failed to upload: {Path(video_file).name}"))
                            
                except ImportError:
                    self.progress_queue.put(("log", "⚠️ TikTok uploader not available. Skipping auto-upload."))
                except Exception as e:
                    self.progress_queue.put(("log", f"❌ Upload error: {e}"))
            
            self.progress_queue.put(("complete", output_files))
            
        except Exception as e:
            self.progress_queue.put(("error", str(e)))
    
    def check_progress_queue(self):
        """Check for progress updates from the generation thread."""
        try:
            while True:
                msg_type, data = self.progress_queue.get_nowait()
                
                if msg_type == "log":
                    self.log_message(data)
                elif msg_type == "complete":
                    self.generation_complete(data)
                    return
                elif msg_type == "error":
                    self.generation_error(data)
                    return
                    
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_progress_queue)
    
    def generation_complete(self, output_files):
        """Handle successful generation completion."""
        self.is_processing = False
        self.generate_button.config(state="normal", text="Generate TikTok Videos")
        self.progress_bar.stop()
        
        messagebox.showinfo("Success", 
                           f"Successfully generated {len(output_files)} TikTok videos!\n\n"
                           f"Output directory: {self.output_dir_path.get()}")
    
    def generation_error(self, error_msg):
        """Handle generation error."""
        self.is_processing = False
        self.generate_button.config(state="normal", text="Generate TikTok Videos")
        self.progress_bar.stop()
        
        self.log_message(f"❌ Error: {error_msg}")
        messagebox.showerror("Error", f"Video generation failed:\n{error_msg}")
    
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()


class SettingsDialog:
    """Settings dialog for configuration."""
    
    def __init__(self, parent, config):
        self.config = config
        self.dialog = Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_dialog()
    
    def setup_dialog(self):
        """Set up the settings dialog."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=BOTH, expand=True)
        
        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=BOTH, expand=True, pady=(0, 20))
        
        # AI Settings tab
        ai_frame = ttk.Frame(notebook)
        notebook.add(ai_frame, text="AI Settings")
        
        ttk.Label(ai_frame, text="OpenAI API Key:").pack(anchor=W, pady=(10, 5))
        self.api_key_var = StringVar(value=self.config.ai.openai_api_key or "")
        ttk.Entry(ai_frame, textvariable=self.api_key_var, show="*", width=50).pack(fill=X, pady=(0, 10))
        
        ttk.Label(ai_frame, text="Narration Style:").pack(anchor=W, pady=(10, 5))
        self.style_var = StringVar(value=self.config.ai.narration_style)
        ttk.Entry(ai_frame, textvariable=self.style_var, width=50).pack(fill=X, pady=(0, 10))
        
        ttk.Label(ai_frame, text="Target Audience:").pack(anchor=W, pady=(10, 5))
        self.audience_var = StringVar(value=self.config.ai.target_audience)
        ttk.Entry(ai_frame, textvariable=self.audience_var, width=50).pack(fill=X, pady=(0, 10))
        
        # Video Settings tab
        video_frame = ttk.Frame(notebook)
        notebook.add(video_frame, text="Video Settings")
        
        ttk.Label(video_frame, text="Video Resolution:").pack(anchor=W, pady=(10, 5))
        res_frame = ttk.Frame(video_frame)
        res_frame.pack(fill=X, pady=(0, 10))
        ttk.Label(res_frame, text="Width:").pack(side=LEFT)
        self.width_var = IntVar(value=self.config.video.width)
        ttk.Entry(res_frame, textvariable=self.width_var, width=10).pack(side=LEFT, padx=5)
        ttk.Label(res_frame, text="Height:").pack(side=LEFT, padx=(10, 0))
        self.height_var = IntVar(value=self.config.video.height)
        ttk.Entry(res_frame, textvariable=self.height_var, width=10).pack(side=LEFT, padx=5)
        
        ttk.Label(video_frame, text="FPS:").pack(anchor=W, pady=(10, 5))
        self.fps_var = IntVar(value=self.config.video.fps)
        ttk.Entry(video_frame, textvariable=self.fps_var, width=10).pack(anchor=W, pady=(0, 10))
        
        # Audio Settings
        ttk.Label(video_frame, text="Narration Volume (0.0 - 1.0):").pack(anchor=W, pady=(10, 5))
        self.narration_vol_var = DoubleVar(value=self.config.video.narration_volume)
        ttk.Scale(video_frame, from_=0.0, to=1.0, variable=self.narration_vol_var, 
                 orient=HORIZONTAL).pack(fill=X, pady=(0, 10))
        
        ttk.Label(video_frame, text="Original Audio Volume (0.0 - 1.0):").pack(anchor=W, pady=(10, 5))
        self.original_vol_var = DoubleVar(value=self.config.video.original_audio_volume)
        ttk.Scale(video_frame, from_=0.0, to=1.0, variable=self.original_vol_var, 
                 orient=HORIZONTAL).pack(fill=X, pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X)
        
        ttk.Button(button_frame, text="Save", command=self.save_settings).pack(side=RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=RIGHT)
    
    def save_settings(self):
        """Save the settings."""
        # Update config
        self.config.ai.openai_api_key = self.api_key_var.get() or None
        self.config.ai.narration_style = self.style_var.get()
        self.config.ai.target_audience = self.audience_var.get()
        
        self.config.video.width = self.width_var.get()
        self.config.video.height = self.height_var.get()
        self.config.video.fps = self.fps_var.get()
        self.config.video.narration_volume = self.narration_vol_var.get()
        self.config.video.original_audio_volume = self.original_vol_var.get()
        
        # Set environment variable if API key is provided
        if self.config.ai.openai_api_key:
            os.environ["OPENAI_API_KEY"] = self.config.ai.openai_api_key
        
        self.dialog.destroy()


def main():
    """Main function to run the GUI."""
    try:
        app = TikTokGeneratorGUI()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication closed by user.")
    except Exception as e:
        print(f"Error running GUI: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()