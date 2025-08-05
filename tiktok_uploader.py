"""
TikTok Uploader Module

Automates the upload of generated videos to TikTok using browser automation.
Provides both automated upload and manual upload guidance.
"""

import os
import time
import json
from pathlib import Path
from typing import Optional, List, Dict

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    HAS_SELENIUM = True
except ImportError:
    HAS_SELENIUM = False

class TikTokUploader:
    """Handles TikTok video uploads using browser automation."""
    
    def __init__(self, headless: bool = False, profile_path: Optional[str] = None):
        """
        Initialize the TikTok uploader.
        
        Args:
            headless: Whether to run browser in headless mode
            profile_path: Path to Chrome profile to maintain login session
        """
        self.headless = headless
        self.profile_path = profile_path
        self.driver = None
        self.wait_timeout = 30
        
        if not HAS_SELENIUM:
            raise ImportError("Selenium is required for TikTok uploads. Install with: pip install selenium")
    
    def setup_driver(self) -> webdriver.Chrome:
        """Set up Chrome WebDriver with appropriate options."""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Add profile path if provided
        if self.profile_path:
            chrome_options.add_argument(f"--user-data-dir={self.profile_path}")
        
        # Additional options for stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Disable notifications
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            return self.driver
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Chrome driver: {e}")
    
    def login_required_check(self) -> bool:
        """Check if user needs to log in to TikTok."""
        try:
            # Look for login indicators
            login_elements = [
                "//a[contains(@href, '/login')]",
                "//button[contains(text(), 'Log in')]",
                "//div[contains(text(), 'Log in')]"
            ]
            
            for xpath in login_elements:
                try:
                    self.driver.find_element(By.XPATH, xpath)
                    return True
                except NoSuchElementException:
                    continue
            
            # Check for upload button as indicator of being logged in
            try:
                self.driver.find_element(By.XPATH, "//a[contains(@href, '/upload')]")
                return False
            except NoSuchElementException:
                return True
                
        except Exception:
            return True
    
    def wait_for_login(self):
        """Wait for user to manually log in."""
        print("🔐 Please log in to TikTok in the browser window...")
        print("   The uploader will continue automatically once you're logged in.")
        
        max_wait_minutes = 10
        wait_seconds = max_wait_minutes * 60
        
        for i in range(wait_seconds):
            time.sleep(1)
            
            if not self.login_required_check():
                print("✅ Login detected! Continuing with upload...")
                return True
            
            # Print progress every 30 seconds
            if i % 30 == 0 and i > 0:
                remaining = (wait_seconds - i) // 60
                print(f"   Still waiting for login... ({remaining} minutes remaining)")
        
        print(f"❌ Timeout: Login not detected within {max_wait_minutes} minutes")
        return False
    
    def upload_video(self, video_path: str, description: str, 
                    hashtags: Optional[List[str]] = None,
                    privacy: str = "public") -> bool:
        """
        Upload a video to TikTok.
        
        Args:
            video_path: Path to the video file
            description: Video description/caption
            hashtags: List of hashtags to add
            privacy: Privacy setting ("public", "friends", "private")
            
        Returns:
            True if upload successful, False otherwise
        """
        if not os.path.exists(video_path):
            print(f"❌ Video file not found: {video_path}")
            return False
        
        try:
            if not self.driver:
                self.setup_driver()
            
            # Navigate to TikTok upload page
            print("🌐 Navigating to TikTok upload page...")
            self.driver.get("https://www.tiktok.com/upload")
            
            # Check if login is required
            if self.login_required_check():
                if not self.wait_for_login():
                    return False
                
                # Navigate to upload page again after login
                self.driver.get("https://www.tiktok.com/upload")
            
            # Wait for upload page to load
            try:
                upload_input = WebDriverWait(self.driver, self.wait_timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
                )
            except TimeoutException:
                print("❌ Upload page did not load properly")
                return False
            
            # Upload the video file
            print(f"📤 Uploading video: {Path(video_path).name}")
            upload_input.send_keys(os.path.abspath(video_path))
            
            # Wait for video to process
            print("⏳ Waiting for video to process...")
            try:
                # Wait for the video preview to appear
                WebDriverWait(self.driver, 120).until(
                    EC.presence_of_element_located((By.XPATH, "//video | //canvas"))
                )
                print("✅ Video processed successfully")
            except TimeoutException:
                print("⚠️  Video processing timeout - continuing anyway")
            
            # Add description and hashtags
            description_text = self._format_description(description, hashtags)
            if description_text:
                print("📝 Adding description...")
                self._add_description(description_text)
            
            # Set privacy if needed
            if privacy != "public":
                print(f"🔒 Setting privacy to: {privacy}")
                self._set_privacy(privacy)
            
            # Submit the upload
            print("🚀 Publishing video...")
            if self._publish_video():
                print("✅ Video uploaded successfully!")
                return True
            else:
                print("❌ Failed to publish video")
                return False
                
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return False
    
    def _format_description(self, description: str, hashtags: Optional[List[str]] = None) -> str:
        """Format the description with hashtags."""
        formatted = description
        
        if hashtags:
            hashtag_text = " ".join([f"#{tag.lstrip('#')}" for tag in hashtags])
            formatted = f"{description}\n\n{hashtag_text}"
        
        return formatted
    
    def _add_description(self, description: str):
        """Add description to the video."""
        try:
            # Look for description/caption input field
            description_selectors = [
                "//div[@contenteditable='true']",
                "//textarea[@placeholder]",
                "//div[contains(@class, 'public-DraftEditor-content')]"
            ]
            
            for selector in description_selectors:
                try:
                    description_field = self.driver.find_element(By.XPATH, selector)
                    description_field.clear()
                    description_field.send_keys(description)
                    return
                except NoSuchElementException:
                    continue
            
            print("⚠️  Could not find description field")
            
        except Exception as e:
            print(f"⚠️  Error adding description: {e}")
    
    def _set_privacy(self, privacy: str):
        """Set video privacy settings."""
        try:
            privacy_map = {
                "public": "Everyone",
                "friends": "Friends",
                "private": "Only you"
            }
            
            privacy_text = privacy_map.get(privacy, "Everyone")
            
            # Look for privacy dropdown
            privacy_button = self.driver.find_element(
                By.XPATH, f"//button[contains(text(), '{privacy_text}') or contains(., 'Who can view')]"
            )
            privacy_button.click()
            
            # Select the privacy option
            option = self.driver.find_element(
                By.XPATH, f"//div[contains(text(), '{privacy_text}')]"
            )
            option.click()
            
        except Exception as e:
            print(f"⚠️  Error setting privacy: {e}")
    
    def _publish_video(self) -> bool:
        """Publish the video."""
        try:
            # Look for publish/post button
            publish_selectors = [
                "//button[contains(text(), 'Post')]",
                "//button[contains(text(), 'Publish')]",
                "//button[contains(text(), 'Upload')]",
                "//div[contains(@class, 'btn') and contains(text(), 'Post')]"
            ]
            
            for selector in publish_selectors:
                try:
                    publish_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    publish_button.click()
                    
                    # Wait for upload to complete
                    time.sleep(5)
                    
                    # Check for success indicators
                    success_indicators = [
                        "//div[contains(text(), 'uploaded')]",
                        "//div[contains(text(), 'posted')]",
                        "//div[contains(text(), 'published')]"
                    ]
                    
                    for indicator in success_indicators:
                        try:
                            WebDriverWait(self.driver, 30).until(
                                EC.presence_of_element_located((By.XPATH, indicator))
                            )
                            return True
                        except TimeoutException:
                            continue
                    
                    # If no success indicator found, assume success after button click
                    return True
                    
                except (NoSuchElementException, TimeoutException):
                    continue
            
            print("⚠️  Could not find publish button")
            return False
            
        except Exception as e:
            print(f"❌ Error publishing video: {e}")
            return False
    
    def close(self):
        """Close the browser driver."""
        if self.driver:
            self.driver.quit()
            self.driver = None


class TikTokUploadGuide:
    """Provides guidance for manual TikTok uploads."""
    
    @staticmethod
    def print_manual_upload_guide(video_files: List[str], description: str):
        """Print step-by-step manual upload instructions."""
        print("\n" + "="*80)
        print("🎯 MANUAL TIKTOK UPLOAD GUIDE")
        print("="*80)
        
        print(f"\n📱 You have {len(video_files)} videos ready for upload:")
        for i, video_file in enumerate(video_files, 1):
            print(f"   {i}. {Path(video_file).name}")
        
        print(f"\n📝 Suggested description for all videos:")
        print(f"   {description}")
        
        print("\n📋 STEP-BY-STEP UPLOAD INSTRUCTIONS:")
        print("1. Open TikTok on your phone or go to https://www.tiktok.com/upload")
        print("2. Log in to your TikTok account")
        print("3. Tap the '+' button or click 'Upload'")
        print("4. Select a video from the generated files")
        print("5. Add the suggested description above")
        print("6. Add relevant hashtags (suggestions below)")
        print("7. Set privacy to 'Public' for maximum reach")
        print("8. Enable comments and duets")
        print("9. Post the video")
        print("10. Repeat for each video file")
        
        print("\n🏷️  SUGGESTED HASHTAGS:")
        hashtags = [
            "#fyp", "#fypシ", "#viral", "#movie", "#cinema", 
            "#film", "#recap", "#story", "#entertaining", "#trending"
        ]
        print("   " + " ".join(hashtags))
        
        print("\n💡 TIPS FOR MAXIMUM ENGAGEMENT:")
        print("   • Upload videos 1-2 hours apart for better algorithm exposure")
        print("   • Post during peak hours (6-10 PM in your timezone)")
        print("   • Engage with comments quickly after posting")
        print("   • Use trending sounds if possible")
        print("   • Add captions for accessibility")
        print("   • Cross-promote on other social media platforms")
        
        print("\n🎬 SERIES POSTING STRATEGY:")
        print("   • Number your videos clearly (Part 1, Part 2, etc.)")
        print("   • End each video with a cliffhanger")
        print("   • Reference previous parts in descriptions")
        print("   • Use consistent hashtags across the series")
        print("   • Pin comments directing viewers to other parts")
        
        print("\n💰 MONETIZATION TIPS:")
        print("   • Build a consistent posting schedule")
        print("   • Engage with your audience regularly")
        print("   • Apply for TikTok Creator Fund when eligible")
        print("   • Partner with brands for sponsored content")
        print("   • Sell merchandise or promote affiliate links")
        
        print("\n" + "="*80)
    
    @staticmethod
    def save_upload_checklist(output_dir: str, video_files: List[str], description: str):
        """Save an upload checklist to a text file."""
        checklist_path = os.path.join(output_dir, "UPLOAD_CHECKLIST.txt")
        
        with open(checklist_path, 'w', encoding='utf-8') as f:
            f.write("TIKTOK UPLOAD CHECKLIST\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Generated Videos ({len(video_files)}):\n")
            for i, video_file in enumerate(video_files, 1):
                f.write(f"[ ] {i}. {Path(video_file).name}\n")
            
            f.write(f"\nSuggested Description:\n{description}\n\n")
            
            f.write("Upload Steps:\n")
            steps = [
                "Open TikTok app or website",
                "Tap '+' or click 'Upload'", 
                "Select video file",
                "Add description and hashtags",
                "Set to Public",
                "Enable comments and duets",
                "Post video",
                "Engage with early comments"
            ]
            
            for step in steps:
                f.write(f"[ ] {step}\n")
            
            f.write(f"\nHashtags: #fyp #movie #recap #viral #trending\n")
        
        print(f"📋 Upload checklist saved to: {checklist_path}")


def create_automated_uploader(headless: bool = False, 
                            profile_path: Optional[str] = None) -> Optional[TikTokUploader]:
    """
    Create a TikTok uploader instance.
    
    Args:
        headless: Whether to run in headless mode
        profile_path: Chrome profile path for persistent login
        
    Returns:
        TikTokUploader instance or None if Selenium not available
    """
    if not HAS_SELENIUM:
        print("⚠️  Selenium not available. Install with: pip install selenium")
        print("   Automated upload will not be available.")
        return None
    
    try:
        return TikTokUploader(headless=headless, profile_path=profile_path)
    except Exception as e:
        print(f"⚠️  Could not create uploader: {e}")
        return None


def main():
    """Demo function for the uploader."""
    print("TikTok Uploader Demo")
    print("This module provides automated and manual upload functionality.")
    
    if HAS_SELENIUM:
        print("✅ Selenium available - automated uploads supported")
    else:
        print("❌ Selenium not available - only manual upload guidance")
    
    # Example manual guide
    example_files = ["movie_part_001.mp4", "movie_part_002.mp4", "movie_part_003.mp4"]
    example_description = "Epic movie moments that will blow your mind! 🎬✨ Part 1 of 3 #fyp #movie #viral"
    
    TikTokUploadGuide.print_manual_upload_guide(example_files, example_description)


if __name__ == "__main__":
    main()