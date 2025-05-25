# Video Translation API

A FastAPI-based service that processes video files, extracts audio, transcribes speech using OpenAI's Whisper API, and translates the content to a specified target language.

## Features

- Upload MP4 video files for processing
- Extract audio tracks from videos
- Transcribe speech using OpenAI Whisper
- Translate content to specified target language
- Async job processing with status tracking
- Docker containerization

## Prerequisites

- Docker
- OpenAI API key

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and add your OpenAI API key
3. Build and run with Docker:

```bash
docker build -t video-translation-api .
docker run -p 8000:8000 --env-file .env video-translation-api
```

## API Endpoints

### POST /upload/
Upload a video file for processing.

**Parameters:**
- `file`: MP4 video file (multipart/form-data)
- `target_language`: Target language code (e.g., 'fr' for French)

**Response:**
```json
{
    "job_id": "uuid-string"
}
```

### GET /upload/status/{job_id}
Get the processing status and results.

**Response:**
```json
{
    "status": "in-progress|error|success",
    "transcription": "Original transcription (if complete)",
    "translation": "Translated text (if complete)",
    "error": "Error message (if failed)"
}
```

## Error Handling

The API includes comprehensive error handling for:
- Invalid file formats
- Failed uploads
- Processing errors
- Invalid job IDs

## Development

To run locally without Docker:

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --reload
``` 