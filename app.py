from flask import Flask, render_template, request, jsonify, send_file, abort
from flask_cors import CORS
import os
import threading
import time
from scraper import YouTubeChannelScraper
import zipfile
import io
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables for progress tracking
scraping_progress = {
    'active': False,
    'current': 0,
    'total': 0,
    'current_video': '',
    'status': 'idle',
    'message': '',
    'results': None
}

def progress_callback(current, total, video_title, status):
    """Callback function to update scraping progress"""
    global scraping_progress
    scraping_progress.update({
        'current': current,
        'total': total,
        'current_video': video_title,
        'status': status
    })

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/scrape', methods=['POST'])
def start_scraping():
    """Start scraping process"""
    global scraping_progress
    
    if scraping_progress['active']:
        return jsonify({'error': 'Scraping already in progress'}), 400
    
    data = request.get_json()
    channel_url = data.get('channel_url')
    max_videos = data.get('max_videos')
    include_timestamps = data.get('include_timestamps', False)
    
    if not channel_url:
        return jsonify({'error': 'Channel URL is required'}), 400
    
    # Reset progress
    scraping_progress.update({
        'active': True,
        'current': 0,
        'total': 0,
        'current_video': '',
        'status': 'starting',
        'message': 'Initializing scraper...',
        'results': None
    })
    
    def scrape_thread():
        global scraping_progress
        try:
            scraper = YouTubeChannelScraper(channel_url)
            scraping_progress['message'] = 'Extracting video information...'
            
            results = scraper.scrape_all_transcripts(
                max_videos=max_videos,
                include_timestamps=include_timestamps,
                progress_callback=progress_callback
            )
            
            scraping_progress.update({
                'active': False,
                'status': 'completed',
                'message': results['message'],
                'results': results
            })
            
        except Exception as e:
            scraping_progress.update({
                'active': False,
                'status': 'error',
                'message': f'Error: {str(e)}',
                'results': None
            })
    
    # Start scraping in background thread
    thread = threading.Thread(target=scrape_thread)
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Scraping started', 'status': 'started'})

@app.route('/api/progress')
def get_progress():
    """Get current scraping progress"""
    return jsonify(scraping_progress)

@app.route('/api/transcripts')
def list_transcripts():
    """List all existing transcripts"""
    scraper = YouTubeChannelScraper("")  # Empty URL since we're just listing files
    transcripts = scraper.get_existing_transcripts()
    return jsonify(transcripts)

@app.route('/api/transcript/<filename>')
def get_transcript(filename):
    """Get content of a specific transcript"""
    scraper = YouTubeChannelScraper("")
    content = scraper.get_transcript_content(filename)
    
    if content is None:
        abort(404)
    
    return jsonify({'filename': filename, 'content': content})

@app.route('/api/download/<filename>')
def download_transcript(filename):
    """Download a specific transcript file"""
    file_path = os.path.join('transcripts', filename)
    
    if not os.path.exists(file_path):
        abort(404)
    
    return send_file(file_path, as_attachment=True)

@app.route('/api/download-all')
def download_all_transcripts():
    """Download all transcripts as a ZIP file"""
    transcripts_dir = 'transcripts'
    
    if not os.path.exists(transcripts_dir) or not os.listdir(transcripts_dir):
        return jsonify({'error': 'No transcripts available'}), 404
    
    # Create ZIP file in memory
    memory_file = io.BytesIO()
    
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename in os.listdir(transcripts_dir):
            file_path = os.path.join(transcripts_dir, filename)
            if os.path.isfile(file_path):
                zf.write(file_path, filename)
    
    memory_file.seek(0)
    
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'transcripts_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
    )

@app.route('/api/clear')
def clear_transcripts():
    """Clear all transcript files"""
    transcripts_dir = 'transcripts'
    
    if os.path.exists(transcripts_dir):
        for filename in os.listdir(transcripts_dir):
            file_path = os.path.join(transcripts_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    
    return jsonify({'message': 'All transcripts cleared'})

if __name__ == '__main__':
    # Create transcripts directory if it doesn't exist
    os.makedirs('transcripts', exist_ok=True)
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

