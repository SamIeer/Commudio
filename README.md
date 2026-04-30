<div align="center">

# 🎤 Commudio

### AI-Powered Speech Analysis Platform for Communication Excellence

Transform your speaking skills with intelligent transcription, speech insights, and actionable AI feedback.

[🌐 Live Demo](https://commudio.vercel.app) • [📘 API Docs](https://commudio-backend.onrender.com/docs) • [🐛 Report Bug](../../issues) • [✨ Request Feature](../../issues)

<br/>

![React](https://img.shields.io/badge/Frontend-React-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Docker](https://img.shields.io/badge/DevOps-Docker-informational)
![License](https://img.shields.io/badge/License-MIT-black)

</div>

---

# 📌 Overview

Commudio is a full-stack AI speech coaching platform that helps users improve communication through audio analysis.

Upload a recording and receive:

* 🎙️ Accurate transcription
* 📊 Speaking metrics (WPM, filler words)
* 🤖 Personalized AI feedback
* 📈 Progress tracking over time

Designed for students, job seekers, creators, and professionals who want to speak better.

https://github.com/user-attachments/assets/816917c2-60c9-4b20-ae3a-1733f8495a2f

---

# ✨ Key Features

## 🎯 Speech Intelligence

* AI transcription using Whisper-class speech models
* Filler word detection (`um`, `uh`, `like`, etc.)
* Speaking speed analysis (Words Per Minute)
* Clear communication insights

## 🤖 AI Feedback Engine

Structured feedback including:

* ✅ Strengths
* ⚠️ Weaknesses
* 🚀 Actionable improvements

## 📊 Analytics Dashboard

* Historical performance trends
* Improvement tracking
* Practice consistency insights
<img width="789" height="683" alt="Screenshot 2026-04-29 223418" src="https://github.com/user-attachments/assets/a222011f-0810-4d98-9a63-64696dcc4f3e" />

## 🔐 Security

* JWT Authentication
* Password hashing
* Protected API routes
* Environment-based secret management
* Production CORS configuration
  <img width="919" height="687" alt="Screenshot 2026-04-29 223320" src="https://github.com/user-attachments/assets/7d28f529-d553-4167-a93d-5620b4f64bf1" />
<img width="659" height="752" alt="Screenshot 2026-04-29 223237" src="https://github.com/user-attachments/assets/58097630-0460-4d37-9234-23e4a9789b94" />


## ⚡ Performance

* Async backend architecture
* Background audio processing
* Dockerized deployment
* Responsive frontend UI

---

# 🖼️ Screenshots

> Add your screenshots here for maximum impact.

| Dashboard | Upload    | Analytics |
| --------- | --------- | --------- |
| <img width="919" height="687" alt="Screenshot 2026-04-29 223320" src="https://github.com/user-attachments/assets/1c6eb3e6-1a75-4951-b978-a6b08b7eeec6" /> | <img width="925" height="690" alt="Screenshot 2026-04-29 223337" src="https://github.com/user-attachments/assets/03f33b31-5519-40c4-a5d1-be11e45aa459" /> | <img width="789" height="683" alt="Screenshot 2026-04-29 223418" src="https://github.com/user-attachments/assets/963cd330-d041-4586-8c8c-578b24370e2c" />
 |
---

# 🏗️ Tech Stack

## Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT Auth
* Pydantic
* Docker

## Frontend

* React
* Vite
* Tailwind CSS
* Axios
* React Router
* Recharts

## AI Layer

* Groq API
* Whisper-based Speech-to-Text
* LLM Feedback Generation

## Deployment

* Frontend: Vercel
* Backend: Render
* Database: Render PostgreSQL

---

# 🧠 System Architecture

```text
React Frontend
      ↓
FastAPI Backend
      ↓
Background Processing
      ↓
Speech Transcription + AI Feedback
      ↓
PostgreSQL Database
```

---

# 📁 Project Structure

```text
commudio/
│
├── backend/
│   └── app/
│       ├── api/
│       ├── core/
│       ├── models/
│       ├── repositories/
│       ├── services/
│       └── schemas/
│
├── frontend/
│   └── src/
│       ├── api/
│       ├── context/
│       ├── pages/
│       ├── components/
│       └── utils/
│
└── docker-compose.yml
```

---

# 🚀 Quick Start

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/commudio.git
cd commudio
```

---

## 2️⃣ Run with Docker

```bash
docker-compose up --build
```

### Access Services

| Service  | URL                        |
| -------- | -------------------------- |
| Frontend | http://localhost:5173      |
| Backend  | http://localhost:8000      |
| API Docs | http://localhost:8000/docs |

---

# ⚙️ Environment Variables

## Backend `.env`

```env
DATABASE_URL=postgresql://...
SECRET_KEY=your_secret_key
GROQ_API_KEY=your_key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

## Frontend `.env`

```env
VITE_API_URL=http://localhost:8000
```

---

# 📡 API Endpoints

## Auth

```text
POST /auth/register
POST /auth/login
GET  /user/me
```

## Recordings

```text
POST   /recordings
GET    /recordings
GET    /recordings/{id}
DELETE /recordings/{id}
```

## Analytics

```text
GET /recordings/stats/summary
GET /recordings/stats/trend
```

---

# 🎯 Use Cases

Commudio is ideal for:

* 🎓 Students preparing presentations
* 💼 Professionals improving communication
* 🎤 Content creators & podcasters
* 🧑‍💼 Interview preparation
* 🗣️ Public speaking practice

---

# 🔒 Security Practices

* Secrets stored in environment variables
* JWT token auth
* Password hashing
* Request validation
* CORS restrictions in production

---

# 📈 Roadmap

* [ ] Real-time processing updates
* [ ] Speech scoring system
* [ ] Multi-language transcription
* [ ] Team dashboard
* [ ] Export PDF feedback reports
* [ ] S3 / Cloud storage integration

---

# 🤝 Contributing

Contributions, issues, and feature requests are welcome.

```bash
Fork → Branch → Commit → Pull Request
```

---

# 📜 License

MIT License

---

# 🙌 Acknowledgements

* FastAPI
* React
* Groq
* Whisper
* PostgreSQL
* Open Source Community

---

<div align="center">

Built with ambition and curiosity.

</div>
