# AI Adaptive Quiz System

## Overview
This project is an AI-powered adaptive quiz system designed for aviation training.

The system dynamically generates questions using AI and adjusts difficulty based on user performance.

## Features
- AI generated questions
- Adaptive difficulty
- 10 level quiz progression
- React frontend dashboard
- Explanation feedback

## Tech Stack
Frontend: React  
Backend: Django REST Framework  
AI API: OpenRouter / LLM API  

## Setup Instructions

### Backend

cd backend  
pip install -r requirements.txt  
python manage.py runserver

### Frontend

cd frontend  
npm install  
npm start

## API Endpoints

POST /api/start-quiz/  
GET /api/question/{session_id}/  
POST /api/submit-answer/

## Difficulty Logic

Level 1–3 → Easy  
Level 4–6 → Medium  
Level 7–10 → Hard