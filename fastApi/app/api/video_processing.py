from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, BackgroundTasks, Request
import uuid
import os
import aiofiles
from typing import Dict
import math
from app.utils import extract_audio_chunk, get_video_duration
from app.services.transcription_service import transcribe_audio
from app.services.translation_service import translate_text

router = APIRouter(prefix="")

UPLOAD_DIR = "uploads"
AUDIO_DIR = "audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

jobs: Dict[str, Dict] = {}

@router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_video(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="MP4 video file"),
    target_language: str = Form(..., description="Target language code, e.g., 'fr' for French")
):
    if not file.filename.endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Only .mp4 files are accepted")

    job_id = str(uuid.uuid4())
    video_path = os.path.join(UPLOAD_DIR, f"{job_id}.mp4")

    try:
        async with aiofiles.open(video_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save uploaded file")

    jobs[job_id] = {
        "status": "in-progress",
        "transcription": None,
        "translation": None,
        "error": None,
    }

    background_tasks.add_task(process_video_job, job_id, video_path, target_language)

    return {"job_id": job_id}

@router.get("/{job_id}")
async def get_job_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID not found")

    response = {
        "status": job["status"],
        "translation": job["translation"],
        "error": job["error"]
    }

    response = {k: v for k, v in response.items() if v is not None}

    return response

async def process_video_job(job_id: str, video_path: str, target_language: str):
    try:
        duration = get_video_duration(video_path)

        chunk_duration = 60  
        chunks_count = math.ceil(duration / chunk_duration)

        full_transcription = ""
        translations = []

        for i in range(chunks_count):
            start_time = i * chunk_duration
            current_chunk_duration = min(chunk_duration, duration - start_time)
            audio_chunk_path = os.path.join(AUDIO_DIR, f"{job_id}_{i}.wav")

            extract_audio_chunk(video_path, audio_chunk_path, start_time, current_chunk_duration)

            transcription = await transcribe_audio(audio_chunk_path)
            full_transcription += transcription + " "

            translation = await translate_text(transcription, target_language)
            translations.append(translation)

            jobs[job_id].update({
                "status": "in-progress",
                "transcription": full_transcription.strip(),
                "translation": "\n".join(translations),
            })

        jobs[job_id].update({
            "status": "success",
            "transcription": full_transcription.strip(),
            "translation": "\n".join(translations),
        })

    except Exception as e:
        jobs[job_id].update({
            "status": "error",
            "error": str(e),
        })
