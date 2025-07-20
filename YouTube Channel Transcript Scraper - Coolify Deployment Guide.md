# YouTube Channel Transcript Scraper - Coolify Deployment Guide

## 🚀 Complete Step-by-Step Deployment Instructions

This guide will walk you through deploying the YouTube Channel Transcript Scraper on Coolify with full Docker containerization.

## 📋 Prerequisites

- Coolify instance running and accessible
- Git repository access (GitHub, GitLab, etc.)
- Basic understanding of Coolify interface

## 🔧 Deployment Methods

### Method 1: Direct GitHub Repository Deployment (Recommended)

1. **Upload to GitHub**
   - Create a new repository on GitHub
   - Upload all the provided files to the repository
   - Ensure the repository is public or accessible to your Coolify instance

2. **Create New Resource in Coolify**
   - Log into your Coolify dashboard
   - Click "New Resource"
   - Select "Public Repository"

3. **Configure Repository**
   - **Repository URL**: `https://github.com/yourusername/youtube-transcript-coolify`
   - **Branch**: `main` (or your default branch)
   - **Build Pack**: Select "Docker Compose"
   - **Docker Compose Location**: `docker-compose.yml`

4. **Environment Variables**
   Set these environment variables in Coolify:
   ```
   FLASK_ENV=production
   PYTHONUNBUFFERED=1
   PORT=5000
   ```

5. **Deploy**
   - Click "Deploy"
   - Monitor the build logs
   - Wait for successful deployment

### Method 2: Local Repository Upload

1. **Prepare Files**
   - Download all provided files
   - Create a directory structure as shown below
   - Upload to your Coolify server

2. **Create Resource**
   - In Coolify, select "Local Repository"
   - Point to the uploaded directory
   - Follow the same configuration as Method 1

## 📁 Required File Structure

Ensure your repository has this exact structure:

```
youtube-transcript-coolify/
├── app.py                    # Flask web application
├── scraper.py               # Core scraping functionality
├── Dockerfile               # Docker container configuration
├── docker-compose.yml       # Docker Compose setup
├── requirements.txt         # Python dependencies
├── coolify.json            # Coolify configuration
├── .dockerignore           # Docker ignore file
├── .env.example            # Environment variables template
├── README.md               # Documentation
├── templates/
│   └── index.html          # Web interface template
└── static/                 # Static assets directory
    ├── css/
    └── js/
```

## ⚙️ Configuration Details

### Docker Configuration
- **Base Image**: Python 3.11 slim
- **Port**: 5000 (internal)
- **Health Check**: `/health` endpoint
- **Volume**: Persistent storage for transcripts
- **User**: Non-root user for security

### Environment Variables
| Variable | Value | Description |
|----------|-------|-------------|
| `FLASK_ENV` | `production` | Flask environment mode |
| `PYTHONUNBUFFERED` | `1` | Python output buffering |
| `PORT` | `5000` | Application port |

### Health Check
- **Endpoint**: `/health`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3

## 🌐 Accessing Your Deployed Application

1. **Get Your URL**
   - After successful deployment, Coolify will provide a URL
   - Format: `https://your-app-name.your-domain.com`

2. **Test the Application**
   - Visit the provided URL
   - You should see the YouTube Channel Transcript Scraper interface
   - Test with a small channel first

## 🔍 Usage Instructions

1. **Enter Channel URL**
   - Supported formats:
     - `https://www.youtube.com/@channelname`
     - `https://www.youtube.com/c/channelname`
     - `https://www.youtube.com/channel/UCxxxxxxxxxxxxxxxxxx`

2. **Configure Options**
   - **Max Videos**: Leave empty for all videos, or set a limit
   - **Include Timestamps**: Check to include timestamps in text files

3. **Start Scraping**
   - Click "Start Scraping"
   - Monitor real-time progress
   - Wait for completion

4. **Download Results**
   - Download individual transcript files
   - Download all transcripts as ZIP
   - View transcripts in browser

## 🛠️ Troubleshooting

### Common Issues

1. **Build Fails**
   - Check Dockerfile syntax
   - Verify all files are present
   - Check build logs in Coolify

2. **Application Won't Start**
   - Verify environment variables
   - Check health check endpoint
   - Review application logs

3. **No Transcripts Found**
   - Some videos don't have transcripts
   - Private videos can't be accessed
   - Try with different channels

### Debugging Steps

1. **Check Logs**
   ```bash
   # In Coolify dashboard, view application logs
   # Look for Python errors or Flask startup issues
   ```

2. **Test Health Endpoint**
   ```bash
   curl https://your-app-url.com/health
   # Should return: {"status":"healthy","timestamp":"..."}
   ```

3. **Verify File Permissions**
   - Ensure transcript directory is writable
   - Check Docker volume mounting

## 📊 Performance Considerations

### Resource Requirements
- **Memory**: 256MB minimum, 512MB recommended
- **CPU**: 0.5 cores minimum, 1 core recommended
- **Storage**: 1GB minimum for transcript storage
- **Network**: Depends on channel size

### Optimization Tips
1. **Set Max Videos**: Limit for testing and smaller deployments
2. **Monitor Storage**: Large channels generate many files
3. **Rate Limiting**: Built-in 1-second delay between requests
4. **Health Monitoring**: Use Coolify's monitoring features

## 🔒 Security Features

- **Non-root User**: Application runs as unprivileged user
- **CORS Enabled**: For web interface functionality
- **Health Checks**: Automatic restart on failure
- **No Sensitive Data**: Only processes public YouTube content

## 🔄 Updates and Maintenance

### Updating the Application
1. **Push Changes**: Update your Git repository
2. **Redeploy**: Trigger redeploy in Coolify
3. **Monitor**: Check logs for successful update

### Backup Considerations
- **Transcripts**: Stored in Docker volume (persistent)
- **Configuration**: Backed up with Git repository
- **Database**: No database required

## 📈 Scaling Options

### Horizontal Scaling
- Deploy multiple instances for different channels
- Use load balancer for high traffic

### Vertical Scaling
- Increase memory for large channels
- Add CPU cores for faster processing

## 🆘 Support and Resources

### Getting Help
1. **Check Logs**: Always start with application logs
2. **Test Locally**: Use provided Docker commands
3. **Verify URLs**: Ensure channel URLs are correct
4. **Community**: Coolify community forums

### Useful Commands
```bash
# Local testing
docker-compose up -d
docker-compose logs -f
docker-compose down

# Health check
curl http://localhost:5000/health

# View transcripts
ls -la transcripts/
```

## ✅ Deployment Checklist

- [ ] All files uploaded to repository
- [ ] Repository accessible to Coolify
- [ ] Environment variables configured
- [ ] Docker Compose selected as build pack
- [ ] Health check endpoint configured
- [ ] Volume mounting for transcripts
- [ ] Application successfully deployed
- [ ] Health endpoint responding
- [ ] Web interface accessible
- [ ] Test scraping with small channel
- [ ] Download functionality working

## 🎯 Success Indicators

Your deployment is successful when:
- ✅ Build completes without errors
- ✅ Health check returns `{"status":"healthy"}`
- ✅ Web interface loads properly
- ✅ Can scrape transcripts from test channel
- ✅ Files download correctly
- ✅ Application restarts automatically on failure

## 📞 Next Steps

After successful deployment:
1. **Test thoroughly** with various channel types
2. **Monitor resource usage** in Coolify dashboard
3. **Set up alerts** for application health
4. **Document your specific configuration** for team use
5. **Consider backup strategy** for important transcripts

Your YouTube Channel Transcript Scraper is now ready for production use! 🎉

