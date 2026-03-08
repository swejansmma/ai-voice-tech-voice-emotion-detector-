# Real-Time Conversation Analytics Hackathon

A simple, real-time conversation analytics website that processes streaming ASR transcripts (or text input) and produces live insights using NLP.

## Features
- **Voice-to-Text**: Real-time recording using WebSpeech API.
- **Sentiment Analysis**: Powered by VADER for accurate emotion detection.
- **Tone Mapping**: Detects if user is Happy, Angry, Urgent, or Confused.
- **Intent & Topic Detection**: Categorizes conversations instantly.
- **Dockerized**: Easy setup with Docker Compose.

## Tech Stack
- **Backend**: Python, FastAPI, WebSockets
- **NLP**: VADER, TextBlob
- **Frontend**: Vanilla JS, HTML5, CSS3
- **Containerization**: Docker, Docker Compose

## Setup
1. Clone the repository.
2. Run `docker compose up --build`.
3. Open `http://localhost:8000`.
