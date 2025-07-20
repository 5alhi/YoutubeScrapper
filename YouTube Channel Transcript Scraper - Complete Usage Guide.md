# YouTube Channel Transcript Scraper - Complete Usage Guide

## Overview
This tool extracts and saves transcripts for every publicly available video on a given YouTube channel. It uses the `youtube-transcript-api` for fetching transcripts and `yt-dlp` for listing all video IDs in the channel.

## Step-by-Step Setup

### 1. Prerequisites
- Python 3.7+ (recommended)
- Internet connection

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/kryptologyst/YouTube-Channel-Transcript-Scraper.git
cd YouTube-Channel-Transcript-Scraper

# Install required dependencies
pip install youtube-transcript-api yt-dlp
```

### 3. Basic Usage

#### Method 1: Modify the Original Script
1. Open `youtube_transcript_scraper.py`
2. Find the line: `channel_url = "INSERT CHANNEL URL HERE"`
3. Replace with your target channel URL: `channel_url = "https://www.youtube.com/@channelname"`
4. Run the script: `python3 youtube_transcript_scraper.py`

#### Method 2: Use the Enhanced Demo Script
The `demo_scraper_fixed.py` includes improvements and better error handling:

```python
from youtube_transcript_api import YouTubeTranscriptApi
from yt_dlp import YoutubeDL
import json
import time
import os

# Simply change the channel_url in the main() function
def main():
    channel_url = "https://www.youtube.com/@YourChannelName"
    scraper = YouTubeChannelScraper(channel_url)
    scraper.scrape_all_transcripts()  # Remove limit parameter for all videos
```

## Channel URL Formats

The scraper accepts various YouTube channel URL formats:
- `https://www.youtube.com/@channelname`
- `https://www.youtube.com/c/channelname`
- `https://www.youtube.com/channel/UCxxxxxxxxxxxxxxxxxx`
- `https://www.youtube.com/user/username`

## Output Files

The scraper creates a `transcripts/` directory with two types of files for each video:

### JSON Files
- Format: `{VIDEO_ID}_transcript.json`
- Contains: Video metadata + full transcript with timestamps
- Example structure:
```json
{
  "video_id": "btWlBHE0pe4",
  "title": "How to communicate clearly",
  "transcript": [
    {
      "text": "You are the only you that's existed",
      "start": 0.0,
      "duration": 2.5
    }
  ]
}
```

### Text Files
- Format: `{Video Title}.txt`
- Contains: Clean, readable transcript
- Includes video title and ID at the top
- Example:
```
Title: How to communicate clearly
Video ID: btWlBHE0pe4
--------------------------------------------------

You are the only you that's existed
in all of human history.
Your experiences are yours
and yours alone.
```

## Advanced Features

### Enable Timestamps in Text Files
To include timestamps in the text output, modify the script:
```python
self.save_transcript(video_id, video_title, transcript, include_timestamps=True)
```

This will produce output like:
```
[00:00:00] You are the only you that's existed
[00:00:02] in all of human history.
```

### Limit Number of Videos (for Testing)
For large channels, you can limit the number of videos processed:
```python
scraper.scrape_all_transcripts(limit=10)  # Process only first 10 videos
```

### Skip Existing Transcripts
The scraper automatically skips videos that already have transcripts saved, making it safe to run multiple times.

## Common Issues and Solutions

### Issue 1: "Could not retrieve a transcript"
**Cause**: Video doesn't have transcripts available (auto-generated or manual)
**Solution**: This is normal - not all videos have transcripts. The script will skip these.

### Issue 2: Rate Limiting
**Cause**: Making too many requests too quickly
**Solution**: The script includes a 1-second delay between requests. For very large channels, you might need to increase this:
```python
time.sleep(2)  # Increase delay to 2 seconds
```

### Issue 3: Private or Members-Only Videos
**Cause**: Video requires login or special access
**Solution**: The script can only access publicly available transcripts.

### Issue 4: Channel Not Found
**Cause**: Incorrect channel URL format
**Solution**: Try different URL formats or verify the channel exists and is public.

## Example Usage Scenarios

### Scenario 1: Educational Content Analysis
```python
# Analyze educational channels
channel_url = "https://www.youtube.com/@TEDEd"
scraper = YouTubeChannelScraper(channel_url)
scraper.scrape_all_transcripts()
```

### Scenario 2: Podcast Transcription
```python
# Get transcripts from podcast channels
channel_url = "https://www.youtube.com/@PodcastChannelName"
scraper = YouTubeChannelScraper(channel_url)
scraper.scrape_all_transcripts()
```

### Scenario 3: Research and Content Creation
```python
# Research specific topics across a channel
channel_url = "https://www.youtube.com/@ResearchChannel"
scraper = YouTubeChannelScraper(channel_url)
scraper.scrape_all_transcripts(limit=50)  # First 50 videos
```

## Performance Tips

1. **Start Small**: Test with a small channel or use the `limit` parameter
2. **Monitor Progress**: The script shows progress for each video
3. **Resume Capability**: Re-running the script will skip already downloaded transcripts
4. **Storage**: Each transcript file is typically 1-10KB, plan storage accordingly

## Troubleshooting

### Debug Mode
Add debug information by modifying the `get_video_ids()` method:
```python
ydl_opts = {
    'extract_flat': True,
    'quiet': False,  # Change to False for debug info
    'playlistend': 10
}
```

### Check Dependencies
Verify installations:
```bash
python3 -c "import youtube_transcript_api; import yt_dlp; print('All dependencies OK')"
```

## Legal and Ethical Considerations

- Only use this tool for publicly available content
- Respect YouTube's Terms of Service
- Consider copyright and fair use when using transcripts
- Be mindful of rate limiting to avoid being blocked

## Support

If you encounter issues:
1. Check that the channel URL is correct and public
2. Verify your internet connection
3. Try with a smaller channel first
4. Check the GitHub repository for updates and issues

## Demo Results

The demo successfully extracted transcripts from TED-Ed channel:
- ✓ "What happens to your brain without any social contact - Terry Kupers"
- ✓ "How to communicate clearly"  
- ✓ "Why is it so hard to get rid of bed bugs - Gale E Ridge"

Each transcript was saved in both JSON and TXT formats in the `transcripts/` directory.

