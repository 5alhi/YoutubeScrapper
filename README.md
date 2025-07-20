# YouTube Channel Transcript Scraper - Coolify Deployment

A containerized web application that extracts transcripts from all videos in a YouTube channel, designed for easy deployment with Coolify.

## Features

- 🎥 **Channel Scraping**: Extract transcripts from entire YouTube channels
- 🌐 **Web Interface**: User-friendly web UI for easy operation
- 📊 **Real-time Progress**: Live progress tracking during scraping
- 📁 **File Management**: Download individual files or all transcripts as ZIP
- 🐳 **Docker Ready**: Fully containerized for easy deployment
- 🔄 **Auto-restart**: Resilient deployment with health checks
- 💾 **Persistent Storage**: Transcripts saved in Docker volumes

## Quick Start with Coolify

### Method 1: Direct Repository Deployment

1. **Add New Resource** in Coolify
2. **Select "Public Repository"**
3. **Repository URL**: `https://github.com/your-username/youtube-transcript-coolify`
4. **Build Pack**: Docker Compose
5. **Deploy**

### Method 2: Manual Setup

1. **Clone this repository** to your Coolify server
2. **Create new resource** in Coolify
3. **Select "Local Repository"**
4. **Point to the cloned directory**
5. **Configure environment variables** (see below)
6. **Deploy**

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `production` | Flask environment |
| `PYTHONUNBUFFERED` | `1` | Python output buffering |
| `PORT` | `5000` | Application port |

## File Structure

```
youtube-transcript-coolify/
├── app.py                 # Flask web application
├── scraper.py            # Core scraping functionality
├── Dockerfile            # Docker container configuration
├── docker-compose.yml    # Docker Compose setup
├── requirements.txt      # Python dependencies
├── coolify.json         # Coolify configuration
├── templates/
│   └── index.html       # Web interface
├── static/              # Static assets (CSS, JS)
└── transcripts/         # Generated transcript files (volume)
```

## Usage

1. **Access the web interface** at your deployed URL
2. **Enter YouTube channel URL** (e.g., `https://www.youtube.com/@channelname`)
3. **Configure options**:
   - Max videos (optional - leave empty for all)
   - Include timestamps (checkbox)
4. **Click "Start Scraping"**
5. **Monitor progress** in real-time
6. **Download results** individually or as ZIP file

## Supported Channel URL Formats

- `https://www.youtube.com/@channelname`
- `https://www.youtube.com/c/channelname`
- `https://www.youtube.com/channel/UCxxxxxxxxxxxxxxxxxx`
- `https://www.youtube.com/user/username`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/health` | GET | Health check |
| `/api/scrape` | POST | Start scraping |
| `/api/progress` | GET | Get scraping progress |
| `/api/transcripts` | GET | List all transcripts |
| `/api/transcript/<filename>` | GET | Get transcript content |
| `/api/download/<filename>` | GET | Download transcript file |
| `/api/download-all` | GET | Download all as ZIP |
| `/api/clear` | GET | Clear all transcripts |

## Docker Commands

### Build locally
```bash
docker build -t youtube-transcript-scraper .
```

### Run locally
```bash
docker-compose up -d
```

### View logs
```bash
docker-compose logs -f
```

### Stop
```bash
docker-compose down
```

## Coolify Configuration

The `coolify.json` file contains all necessary configuration for Coolify deployment:

- **Health checks** on `/health` endpoint
- **Volume mounting** for persistent transcript storage
- **Environment variables** setup
- **Port mapping** configuration
- **Restart policies** for reliability

## Storage

- Transcripts are stored in a Docker volume (`transcript_data`)
- Files persist across container restarts
- Both JSON (with metadata) and TXT (readable) formats are generated
- Automatic file naming based on video titles

## Troubleshooting

### Common Issues

1. **"No transcripts available"**
   - Some videos don't have auto-generated transcripts
   - Private/restricted videos can't be accessed
   - This is normal behavior

2. **Rate limiting**
   - Built-in 1-second delay between requests
   - For large channels, scraping may take time

3. **Memory usage**
   - Large channels may require more memory
   - Consider setting max_videos limit for testing

### Logs

Check application logs in Coolify dashboard or via Docker:
```bash
docker-compose logs youtube-transcript-scraper
```

### Health Check

The application includes a health check endpoint at `/health` that returns:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

## Development

### Local Development Setup

1. **Clone repository**
```bash
git clone <repository-url>
cd youtube-transcript-coolify
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run locally**
```bash
python app.py
```

4. **Access at** `http://localhost:5000`

### Testing

Test the scraper with a small educational channel:
```bash
curl -X POST http://localhost:5000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"channel_url": "https://www.youtube.com/@TEDEd", "max_videos": 3}'
```

## Security Considerations

- Application runs as non-root user in container
- No sensitive data stored (only public YouTube transcripts)
- CORS enabled for web interface functionality
- Health checks ensure service availability

## Performance

- **Memory**: ~100-200MB base usage
- **CPU**: Low usage, spikes during scraping
- **Storage**: ~1-10KB per transcript file
- **Network**: Depends on channel size and video count

## License

This project is open source. Feel free to modify and distribute.

## Support

For issues and questions:
1. Check the logs in Coolify dashboard
2. Verify YouTube channel URL format
3. Test with smaller channels first
4. Ensure sufficient disk space for transcripts

