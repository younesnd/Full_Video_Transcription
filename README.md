# 🎬 Video Transcription App

A full-stack video transcription application built with FastAPI backend and Next.js frontend, containerized with Docker for easy deployment.

## 🏗️ Architecture

This application consists of two main components:

- **Backend**: FastAPI server that handles video processing and transcription
- **Frontend**: Next.js web interface for uploading videos and displaying results

## 📁 Project Structure

```
video-transcription-app/
├── docker-compose.yml          # Docker orchestration configuration
├── fastApi/                    # Backend service
│   ├── Dockerfile
│   └── [API source code]
└── Video_Transcription_Frontend/  # Frontend service
    ├── Dockerfile
    └── [Next.js source code]
```

## 🚀 Quick Start

### Prerequisites

Before running the application, ensure you have:

- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

### Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/younesnd/Full_Video_Transcription.git
   cd Full_Video_Transcription
   ```

2. **Start the application**

   ```bash
   docker compose up --build
   ```

   This command will:

   - Build both frontend and backend Docker images
   - Start the containers
   - Set up networking between services

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 🧪 Testing the Application

1. Open your browser and navigate to http://localhost:3000
2. Use the upload interface to select a video file
3. Submit the video for transcription
4. The frontend will communicate with the backend API to process your video
5. View the transcription results in the web interface

## 📋 Available Services

| Service  | URL                   | Description               |
| -------- | --------------------- | ------------------------- |
| Frontend | http://localhost:3000 | Web interface for uploads |
| Backend  | http://localhost:8000 | API endpoints and docs    |

## 🛠️ Development

### Viewing API Documentation

FastAPI automatically generates interactive API documentation available at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Making Changes

When you modify the code:

- Frontend changes will be hot-reloaded automatically
- Backend changes require restarting the containers:
  ```bash
  docker compose restart
  ```

## 🛑 Stopping the Application

To stop all services:

```bash
docker compose down
```

To stop and remove all containers, networks, and volumes:

```bash
docker compose down --volumes --remove-orphans
```

## 🔧 Troubleshooting

**Port conflicts**: If ports 3000 or 8000 are already in use, modify the port mappings in `docker-compose.yml`

**Build issues**: Try rebuilding with no cache:

```bash
docker compose build --no-cache
docker compose up
```

**Container logs**: View logs to debug issues:

```bash
docker compose logs [service-name]
```

## 📝 Additional Notes

- Ensure sufficient disk space for Docker images and video processing
- Large video files may take longer to process depending on your system resources
- The application supports common video formats (check backend documentation for specific format support)
