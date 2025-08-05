#!/usr/bin/env python3
"""
Web-based GUI interface for TikTok Video Generator

A simple web interface using Flask that allows non-technical users to easily
convert movies into TikTok videos without needing to use command line.
"""

import os
import threading
import time
from pathlib import Path
import queue

try:
    from flask import Flask, render_template_string, request, jsonify, send_from_directory
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False

try:
    from tiktok_generator import TikTokVideoGenerator
    from config import Config
    from tiktok_uploader import TikTokUploadGuide
    HAS_GENERATOR = True
except ImportError:
    HAS_GENERATOR = False

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TikTok Video Generator</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #4a5568;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .header p {
            color: #718096;
            font-size: 1.1em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #4a5568;
        }
        .form-group input[type="text"], 
        .form-group input[type="file"], 
        .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        .form-row {
            display: flex;
            gap: 20px;
        }
        .form-row .form-group {
            flex: 1;
        }
        .slider-container {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .slider {
            flex: 1;
            -webkit-appearance: none;
            height: 8px;
            border-radius: 5px;
            background: #e2e8f0;
            outline: none;
        }
        .slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
        }
        .slider-value {
            min-width: 40px;
            text-align: center;
            font-weight: 600;
            color: #4a5568;
        }
        .checkbox-container {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 15px;
        }
        .checkbox-container input[type="checkbox"] {
            width: auto;
            transform: scale(1.2);
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            margin: 10px 5px;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .btn:disabled {
            background: #a0aec0;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        .btn-secondary {
            background: #4a5568;
        }
        .btn-secondary:hover {
            box-shadow: 0 5px 15px rgba(74, 85, 104, 0.4);
        }
        .progress-container {
            margin-top: 30px;
            padding: 20px;
            background: #f7fafc;
            border-radius: 8px;
            border: 2px solid #e2e8f0;
        }
        .progress-bar {
            width: 100%;
            height: 20px;
            background: #e2e8f0;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 15px;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            width: 0%;
            transition: width 0.3s ease;
        }
        .log-output {
            background: #1a202c;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 8px;
            height: 300px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            white-space: pre-wrap;
        }
        .status {
            padding: 10px 15px;
            border-radius: 5px;
            margin-bottom: 15px;
            font-weight: 600;
        }
        .status.success {
            background: #c6f6d5;
            color: #22543d;
            border: 1px solid #9ae6b4;
        }
        .status.error {
            background: #fed7d7;
            color: #742a2a;
            border: 1px solid #fc8181;
        }
        .status.warning {
            background: #fef5e7;
            color: #744210;
            border: 1px solid #f6e05e;
        }
        .hidden {
            display: none;
        }
        .file-info {
            background: #ebf8ff;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
            border-left: 4px solid #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 TikTok Video Generator</h1>
            <p>Transform movies into engaging TikTok content with AI narration</p>
        </div>

        <form id="videoForm">
            <div class="form-group">
                <label for="videoFile">📁 Select Video File</label>
                <input type="file" id="videoFile" name="videoFile" accept="video/*" required>
                <div id="fileInfo" class="file-info hidden"></div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="outputDir">📂 Output Directory</label>
                    <input type="text" id="outputDir" name="outputDir" value="./tiktok_videos" required>
                </div>
                <div class="form-group">
                    <label for="videoTitle">🎯 Video Title (optional)</label>
                    <input type="text" id="videoTitle" name="videoTitle" placeholder="Leave empty to use filename">
                </div>
            </div>

            <div class="form-group">
                <label for="duration">⏱️ Segment Duration: <span id="durationValue">30</span> seconds</label>
                <div class="slider-container">
                    <span>15s</span>
                    <input type="range" id="duration" name="duration" min="15" max="60" value="30" class="slider">
                    <span>60s</span>
                </div>
            </div>

            <div class="checkbox-container">
                <input type="checkbox" id="autoUpload" name="autoUpload">
                <label for="autoUpload">🚀 Enable automatic TikTok upload (experimental)</label>
            </div>

            <div style="text-align: center; margin-top: 30px;">
                <button type="submit" class="btn" id="generateBtn">
                    🎬 Generate TikTok Videos
                </button>
                <button type="button" class="btn btn-secondary" onclick="showUploadGuide()">
                    📖 Upload Guide
                </button>
                <button type="button" class="btn btn-secondary" onclick="openOutputFolder()" id="openFolderBtn" style="display: none;">
                    📁 Open Output Folder
                </button>
            </div>
        </form>

        <div id="progressContainer" class="progress-container hidden">
            <h3>🔄 Processing...</h3>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <div class="log-output" id="logOutput"></div>
        </div>

        <div id="statusContainer"></div>
    </div>

    <script>
        let isProcessing = false;
        let checkInterval = null;

        // Update duration display
        document.getElementById('duration').oninput = function() {
            document.getElementById('durationValue').textContent = this.value;
        };

        // File input change handler
        document.getElementById('videoFile').onchange = function() {
            const file = this.files[0];
            const fileInfo = document.getElementById('fileInfo');
            
            if (file) {
                const sizeGB = (file.size / (1024 * 1024 * 1024)).toFixed(2);
                const sizeMB = (file.size / (1024 * 1024)).toFixed(1);
                
                fileInfo.innerHTML = `
                    <strong>Selected:</strong> ${file.name}<br>
                    <strong>Size:</strong> ${sizeGB > 1 ? sizeGB + ' GB' : sizeMB + ' MB'}<br>
                    <strong>Type:</strong> ${file.type || 'Unknown'}
                `;
                fileInfo.classList.remove('hidden');
                
                // Auto-set title if empty
                const titleInput = document.getElementById('videoTitle');
                if (!titleInput.value) {
                    const name = file.name.replace(/\.[^/.]+$/, ""); // Remove extension
                    titleInput.value = name;
                }
            } else {
                fileInfo.classList.add('hidden');
            }
        };

        // Form submission
        document.getElementById('videoForm').onsubmit = async function(e) {
            e.preventDefault();
            
            if (isProcessing) return;
            
            const formData = new FormData(this);
            const generateBtn = document.getElementById('generateBtn');
            const progressContainer = document.getElementById('progressContainer');
            const statusContainer = document.getElementById('statusContainer');
            
            // Reset UI
            statusContainer.innerHTML = '';
            progressContainer.classList.remove('hidden');
            generateBtn.disabled = true;
            generateBtn.textContent = '🔄 Processing...';
            isProcessing = true;
            
            // Clear log
            document.getElementById('logOutput').textContent = '';
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    // Start checking progress
                    startProgressCheck();
                } else {
                    const error = await response.text();
                    showStatus('error', 'Error: ' + error);
                    resetUI();
                }
            } catch (error) {
                showStatus('error', 'Network error: ' + error.message);
                resetUI();
            }
        };

        function startProgressCheck() {
            checkInterval = setInterval(async () => {
                try {
                    const response = await fetch('/progress');
                    const data = await response.json();
                    
                    // Update log
                    if (data.logs) {
                        const logOutput = document.getElementById('logOutput');
                        logOutput.textContent = data.logs.join('\n');
                        logOutput.scrollTop = logOutput.scrollHeight;
                    }
                    
                    // Update progress bar
                    if (data.progress !== undefined) {
                        document.getElementById('progressFill').style.width = data.progress + '%';
                    }
                    
                    // Check if complete
                    if (data.status === 'complete') {
                        clearInterval(checkInterval);
                        showStatus('success', `✅ Successfully generated ${data.video_count} TikTok videos!`);
                        document.getElementById('openFolderBtn').style.display = 'inline-block';
                        resetUI();
                    } else if (data.status === 'error') {
                        clearInterval(checkInterval);
                        showStatus('error', '❌ Error: ' + data.error);
                        resetUI();
                    }
                } catch (error) {
                    console.error('Progress check error:', error);
                }
            }, 1000);
        }

        function resetUI() {
            const generateBtn = document.getElementById('generateBtn');
            generateBtn.disabled = false;
            generateBtn.textContent = '🎬 Generate TikTok Videos';
            isProcessing = false;
        }

        function showStatus(type, message) {
            const statusContainer = document.getElementById('statusContainer');
            statusContainer.innerHTML = `<div class="status ${type}">${message}</div>`;
        }

        function showUploadGuide() {
            window.open('/upload-guide', '_blank');
        }

        function openOutputFolder() {
            const outputDir = document.getElementById('outputDir').value;
            window.open('/open-folder?path=' + encodeURIComponent(outputDir), '_blank');
        }

        // Check dependencies on load
        window.onload = async function() {
            try {
                const response = await fetch('/status');
                const data = await response.json();
                
                if (!data.dependencies_ok) {
                    showStatus('warning', '⚠️ Some dependencies are missing. Please install requirements: pip install -r requirements.txt');
                    document.getElementById('generateBtn').disabled = true;
                } else if (!data.api_key_configured) {
                    showStatus('warning', '⚠️ OpenAI API key not configured. AI features will be limited.');
                } else {
                    showStatus('success', '✅ TikTok Video Generator ready!');
                }
            } catch (error) {
                showStatus('error', 'Unable to check system status');
            }
        };
    </script>
</body>
</html>
"""

class TikTokWebGUI:
    """Web-based GUI for TikTok video generation."""
    
    def __init__(self, host='127.0.0.1', port=5000):
        if not HAS_FLASK:
            raise ImportError("Flask is required for web GUI. Install with: pip install flask")
        
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.app.secret_key = 'tiktok_generator_secret_key'
        
        # Generation state
        self.is_processing = False
        self.progress_logs = []
        self.progress_percentage = 0
        self.generation_result = None
        
        # Setup routes
        self.setup_routes()
    
    def setup_routes(self):
        """Set up Flask routes."""
        
        @self.app.route('/')
        def index():
            return render_template_string(HTML_TEMPLATE)
        
        @self.app.route('/status')
        def status():
            config = Config() if HAS_GENERATOR else None
            return jsonify({
                'dependencies_ok': HAS_GENERATOR,
                'api_key_configured': config.validate() if config else False,
                'flask_available': HAS_FLASK
            })
        
        @self.app.route('/generate', methods=['POST'])
        def generate():
            if self.is_processing:
                return "Already processing", 400
            
            if not HAS_GENERATOR:
                return "Generator dependencies missing", 400
            
            try:
                # Get form data
                video_file = request.files.get('videoFile')
                output_dir = request.form.get('outputDir', './tiktok_videos')
                video_title = request.form.get('videoTitle', '').strip() or None
                duration = int(request.form.get('duration', 30))
                auto_upload = request.form.get('autoUpload') == 'on'
                
                if not video_file:
                    return "No video file provided", 400
                
                # Save uploaded file
                upload_dir = '/tmp/tiktok_uploads'
                os.makedirs(upload_dir, exist_ok=True)
                input_path = os.path.join(upload_dir, video_file.filename)
                video_file.save(input_path)
                
                # Start generation in background thread
                thread = threading.Thread(
                    target=self.generate_videos_thread,
                    args=(input_path, output_dir, video_title, duration, auto_upload)
                )
                thread.daemon = True
                thread.start()
                
                return "Generation started", 200
                
            except Exception as e:
                return f"Error starting generation: {e}", 500
        
        @self.app.route('/progress')
        def progress():
            return jsonify({
                'status': 'processing' if self.is_processing else 'complete' if self.generation_result else 'idle',
                'logs': self.progress_logs,
                'progress': self.progress_percentage,
                'video_count': len(self.generation_result) if self.generation_result else 0,
                'error': getattr(self.generation_result, 'error', None) if hasattr(self.generation_result, 'error') else None
            })
        
        @self.app.route('/upload-guide')
        def upload_guide():
            try:
                with open('UPLOAD_GUIDE.md', 'r', encoding='utf-8') as f:
                    content = f.read()
                # Convert markdown to HTML (basic)
                content = content.replace('\n', '<br>')
                content = content.replace('# ', '<h1>').replace('\n<br>', '</h1>\n')
                content = content.replace('## ', '<h2>').replace('\n<br>', '</h2>\n')
                content = content.replace('### ', '<h3>').replace('\n<br>', '</h3>\n')
                return f"<html><body style='font-family: Arial; padding: 20px; max-width: 800px; margin: 0 auto;'>{content}</body></html>"
            except FileNotFoundError:
                return "Upload guide not found", 404
        
        @self.app.route('/open-folder')
        def open_folder():
            path = request.args.get('path', './tiktok_videos')
            if os.path.exists(path):
                return f"<script>alert('Output folder: {path}\\nPlease navigate to this folder manually.');</script>"
            else:
                return f"<script>alert('Folder does not exist: {path}');</script>"
    
    def add_log(self, message):
        """Add a log message."""
        self.progress_logs.append(f"[{time.strftime('%H:%M:%S')}] {message}")
        # Keep only last 100 logs
        if len(self.progress_logs) > 100:
            self.progress_logs = self.progress_logs[-100:]
    
    def generate_videos_thread(self, input_path, output_dir, video_title, duration, auto_upload):
        """Thread function for video generation."""
        try:
            self.is_processing = True
            self.progress_logs = []
            self.generation_result = None
            self.progress_percentage = 0
            
            self.add_log("🎬 Starting video generation...")
            self.add_log(f"Input: {os.path.basename(input_path)}")
            self.add_log(f"Output: {output_dir}")
            self.add_log(f"Duration: {duration}s")
            
            # Initialize configuration
            config = Config()
            config.video.segment_duration = duration
            
            # Initialize generator
            generator = TikTokVideoGenerator(config)
            
            self.progress_percentage = 20
            self.add_log("🔄 Processing video segments...")
            
            # Generate videos
            output_files = generator.generate_videos(
                input_video=input_path,
                output_dir=output_dir,
                video_title=video_title
            )
            
            self.progress_percentage = 80
            self.add_log(f"✅ Generated {len(output_files)} video segments")
            
            # Generate description
            title = video_title or Path(input_path).stem
            description = generator.generate_description(title, len(output_files))
            self.add_log(f"📝 Generated description and hashtags")
            
            # Create upload guide
            TikTokUploadGuide.save_upload_checklist(output_dir, output_files, description)
            self.add_log(f"📋 Created upload checklist")
            
            # Auto-upload if enabled
            if auto_upload:
                self.add_log("🚀 Auto-upload feature coming soon!")
                self.add_log("For now, please use the manual upload guide")
            
            self.progress_percentage = 100
            self.generation_result = output_files
            self.add_log(f"🎉 Generation complete! {len(output_files)} videos ready")
            
        except Exception as e:
            self.add_log(f"❌ Error: {e}")
            self.generation_result = type('obj', (object,), {'error': str(e)})
        finally:
            self.is_processing = False
    
    def run(self, debug=False):
        """Run the web application."""
        print(f"🌐 Starting TikTok Video Generator Web Interface...")
        print(f"   Open your browser and go to: http://{self.host}:{self.port}")
        print(f"   Press Ctrl+C to stop the server")
        
        try:
            self.app.run(host=self.host, port=self.port, debug=debug)
        except Exception as e:
            print(f"❌ Error starting web server: {e}")

def main():
    """Main function to run the web GUI."""
    if not HAS_FLASK:
        print("❌ Flask is required for web GUI")
        print("   Install with: pip install flask")
        return False
    
    try:
        gui = TikTokWebGUI()
        gui.run()
        return True
    except KeyboardInterrupt:
        print("\n👋 Web server stopped")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()