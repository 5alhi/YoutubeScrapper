from youtube_transcript_api import YouTubeTranscriptApi
from yt_dlp import YoutubeDL
import json
import time
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeChannelScraper:
    def __init__(self, channel_url, output_dir="transcripts"):
        self.channel_url = channel_url
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"Created output directory: {self.output_dir}")

    def get_video_ids(self, max_videos=None):
        """Extract all video IDs and titles from the channel's uploads"""
        ydl_opts = {
            'extract_flat': True,
            'quiet': True,
        }
        
        if max_videos:
            ydl_opts['playlistend'] = max_videos
        
        with YoutubeDL(ydl_opts) as ydl:
            try:
                # Add /videos to get the uploads playlist
                if not self.channel_url.endswith('/videos'):
                    channel_url = self.channel_url + '/videos'
                else:
                    channel_url = self.channel_url
                    
                logger.info(f"Extracting video information from: {channel_url}")
                
                # Get channel information
                channel_info = ydl.extract_info(channel_url, download=False)
                
                # Extract video IDs and titles
                videos = []
                if 'entries' in channel_info:
                    for entry in channel_info['entries']:
                        if entry and entry.get('id') and entry.get('title'):
                            # Clean the title to make it filesystem-friendly
                            clean_title = "".join(c for c in entry['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
                            videos.append({
                                'id': entry['id'],
                                'title': clean_title,
                                'original_title': entry['title']
                            })
                
                logger.info(f"Found {len(videos)} videos")
                return videos
            except Exception as e:
                logger.error(f"Error getting video information: {str(e)}")
                return []

    def get_transcript(self, video_id):
        """Get transcript for a single video"""
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript
        except Exception as e:
            logger.warning(f"Error getting transcript for video {video_id}: {str(e)}")
            return None

    def save_transcript(self, video_id, video_title, original_title, transcript, include_timestamps=False):
        """Save transcript to both JSON and TXT files using video title"""
        # Save JSON version (keep ID version for reference)
        json_filename = os.path.join(self.output_dir, f"{video_id}_transcript.json")
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump({
                'video_id': video_id,
                'title': original_title,
                'clean_title': video_title,
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'scraped_at': datetime.now().isoformat(),
                'transcript': transcript
            }, f, ensure_ascii=False, indent=2)
        
        # Save plain text version with title
        txt_filename = os.path.join(self.output_dir, f"{video_title}.txt")
        with open(txt_filename, 'w', encoding='utf-8') as f:
            # Write title at the top
            f.write(f"Title: {original_title}\n")
            f.write(f"Video ID: {video_id}\n")
            f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
            f.write(f"Scraped: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 50 + "\n\n")
            
            # Write each transcript segment
            for entry in transcript:
                if include_timestamps:
                    hours = int(entry['start'] // 3600)
                    minutes = int((entry['start'] % 3600) // 60)
                    seconds = int(entry['start'] % 60)
                    timestamp = f"[{hours:02d}:{minutes:02d}:{seconds:02d}] "
                    f.write(f"{timestamp}{entry['text']}\n")
                else:
                    f.write(f"{entry['text']}\n")

    def scrape_all_transcripts(self, max_videos=None, include_timestamps=False, progress_callback=None):
        """Scrape transcripts from all videos in the channel"""
        videos = self.get_video_ids(max_videos)
        
        if not videos:
            logger.error("No videos found or unable to extract video information")
            return {"success": False, "message": "No videos found", "processed": 0, "successful": 0}

        successful_downloads = 0
        processed = 0
        
        for i, video in enumerate(videos, 1):
            video_id = video['id']
            video_title = video['title']
            original_title = video['original_title']
            
            logger.info(f"Processing video {i}/{len(videos)}: {original_title}")
            
            # Check if transcript already exists
            if os.path.exists(os.path.join(self.output_dir, f"{video_title}.txt")):
                logger.info("Transcript already exists, skipping...")
                processed += 1
                successful_downloads += 1
                if progress_callback:
                    progress_callback(i, len(videos), video_title, "skipped")
                continue

            transcript = self.get_transcript(video_id)
            if transcript:
                self.save_transcript(video_id, video_title, original_title, transcript, include_timestamps)
                logger.info(f"✓ Saved transcript for: {original_title}")
                successful_downloads += 1
                if progress_callback:
                    progress_callback(i, len(videos), video_title, "success")
            else:
                logger.warning(f"✗ Could not get transcript for: {original_title}")
                if progress_callback:
                    progress_callback(i, len(videos), video_title, "failed")
            
            processed += 1
            
            # Add a small delay to avoid rate limiting
            time.sleep(1)
            
        result = {
            "success": True,
            "message": f"Completed! Successfully downloaded {successful_downloads} out of {processed} transcripts.",
            "processed": processed,
            "successful": successful_downloads,
            "total_found": len(videos)
        }
        
        logger.info(result["message"])
        return result

    def get_existing_transcripts(self):
        """Get list of existing transcript files"""
        transcripts = []
        if os.path.exists(self.output_dir):
            for filename in os.listdir(self.output_dir):
                if filename.endswith('.txt'):
                    file_path = os.path.join(self.output_dir, filename)
                    file_size = os.path.getsize(file_path)
                    modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    transcripts.append({
                        'filename': filename,
                        'title': filename.replace('.txt', ''),
                        'size': file_size,
                        'modified': modified_time.isoformat(),
                        'path': file_path
                    })
        
        return sorted(transcripts, key=lambda x: x['modified'], reverse=True)

    def get_transcript_content(self, filename):
        """Get content of a specific transcript file"""
        file_path = os.path.join(self.output_dir, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        return None

