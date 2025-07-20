from youtube_transcript_api import YouTubeTranscriptApi
from yt_dlp import YoutubeDL
import json
import time
import os

class YouTubeChannelScraper:
    def __init__(self, channel_url):
        self.channel_url = channel_url
        self.output_dir = "transcripts"
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def get_video_ids(self):
        """Extract all video IDs and titles from the channel's uploads"""
        ydl_opts = {
            'extract_flat': True,
            'quiet': True,
            'playlistend': 10  # Limit to first 10 videos for demo
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            try:
                # Add /videos to get the uploads playlist
                if not self.channel_url.endswith('/videos'):
                    channel_url = self.channel_url + '/videos'
                else:
                    channel_url = self.channel_url
                    
                print(f"Extracting video information from: {channel_url}")
                
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
                                'title': clean_title
                            })
                
                return videos
            except Exception as e:
                print(f"Error getting video information: {str(e)}")
                return []

    def get_transcript(self, video_id):
        """Get transcript for a single video"""
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript
        except Exception as e:
            print(f"Error getting transcript for video {video_id}: {str(e)}")
            return None

    def save_transcript(self, video_id, video_title, transcript, include_timestamps=False):
        """Save transcript to both JSON and TXT files using video title"""
        # Save JSON version (keep ID version for reference)
        json_filename = os.path.join(self.output_dir, f"{video_id}_transcript.json")
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump({
                'video_id': video_id,
                'title': video_title,
                'transcript': transcript
            }, f, ensure_ascii=False, indent=2)
        
        # Save plain text version with title
        txt_filename = os.path.join(self.output_dir, f"{video_title}.txt")
        with open(txt_filename, 'w', encoding='utf-8') as f:
            # Write title at the top
            f.write(f"Title: {video_title}\n")
            f.write(f"Video ID: {video_id}\n")
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

    def scrape_all_transcripts(self, limit=None):
        """Scrape transcripts from all videos in the channel"""
        videos = self.get_video_ids()
        print(f"Found {len(videos)} videos")
        
        # Limit for demo purposes
        if limit:
            videos = videos[:limit]
            print(f"Processing first {limit} videos for demo")

        successful_downloads = 0
        for i, video in enumerate(videos, 1):
            video_id = video['id']
            video_title = video['title']
            print(f"Processing video {i}/{len(videos)}: {video_title}")
            
            # Check if transcript already exists
            if os.path.exists(os.path.join(self.output_dir, f"{video_title}.txt")):
                print("Transcript already exists, skipping...")
                continue

            transcript = self.get_transcript(video_id)
            if transcript:
                self.save_transcript(video_id, video_title, transcript)
                print(f"✓ Saved transcript for: {video_title}")
                successful_downloads += 1
            else:
                print(f"✗ Could not get transcript for: {video_title}")
            
            # Add a small delay to avoid rate limiting
            time.sleep(1)
            
        print(f"\nCompleted! Successfully downloaded {successful_downloads} transcripts.")

def main():
    # Demo with a channel that has good transcripts - using TED-Ed
    channel_url = "https://www.youtube.com/@TEDEd"
    scraper = YouTubeChannelScraper(channel_url)
    
    # Limit to first 3 videos for demo
    scraper.scrape_all_transcripts(limit=3)

if __name__ == "__main__":
    main()

