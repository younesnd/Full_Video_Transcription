# 🎬 Video Transcription App (FastAPI + Next.js)

This is a simple video transcription app composed of a FastAPI backend and a Next.js frontend. It uses Docker Compose to run both services easily.

---

## 📦 Project Structure

.
├── docker-compose.yml
├── fastApi/ # FastAPI backend
│ └── Dockerfile
├── Video_Transcription_Frontend/ # Next.js frontend
│ └── Dockerfile

````

---

## 🚀 How to Run the App### 1. Prerequisites

- Docker
- Docker Compose

### 2. Clone the repository

```bash
git clone https://github.com/younesnd/Full_Video_Transcription.git
cd Full_Video_Transcription

````

### 3. Start the application```bash

docker compose up --build

````

---

## 🌐 App URLs

| Service | URL |
| --- | --- |
| Frontend | [http://localhost:3000](http://localhost:3000/) |
| Backend | [http://localhost:8000](http://localhost:8000/) |

---

## 🧪 How to Test

1. Visit [http://localhost:3000](http://localhost:3000/)
2. Upload a video file using the UI
3. The app will call the backend and process the transcription

---

## 🛑 Stopping the App

To stop the app:

```bash
docker compose down
````
