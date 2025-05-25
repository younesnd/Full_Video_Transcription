import subprocess


def get_video_duration(video_path: str) -> float:
    """Use ffprobe to get video duration in seconds."""
    import subprocess
    command = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")
    return float(result.stdout.strip())

def extract_audio_chunk(video_path: str, audio_path: str, start_time: float, duration: float):
    """Extract a chunk of audio from the video starting at start_time with given duration."""
    command = [
        "ffmpeg",
        "-ss", str(start_time),
        "-t", str(duration),
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path,
        "-y"
    ]
    print(f"Running command: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"ffmpeg stdout:\n{result.stdout}")
        print(f"ffmpeg stderr:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg failed with return code {e.returncode}")
        print(f"ffmpeg stderr:\n{e.stderr}")
        raise
