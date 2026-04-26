<div align="center">
🎤 Commudio
AI-Powered Speech Analysis Platform for Communication Excellence
Show Image
Show Image
Show Image
Show Image
Transform your communication skills with AI-powered speech analysis, real-time feedback, and actionable insights.
Live Demo · Report Bug · Request Feature
Show Image
</div>

📋 Table of Contents

✨ Features
🎯 Why Commudio?
🚀 Demo
🏗️ Tech Stack
📸 Screenshots
🔧 Installation

Prerequisites
Backend Setup
Frontend Setup
Docker Setup


⚙️ Configuration
🎯 Usage
🔐 Admin Panel
📊 API Documentation
🏛️ Architecture
🔒 Security
🧪 Testing
📈 Performance
🚢 Deployment
🤝 Contributing
📜 License
👥 Team
🙏 Acknowledgments


✨ Features
🎯 Core Features

🎙️ Audio Transcription - Powered by Groq's Whisper API for accurate speech-to-text
📊 Speech Analysis - Real-time WPM (Words Per Minute) calculation
💬 Filler Word Detection - Track and reduce "um", "uh", "like", etc.
🤖 AI Feedback - Personalized improvement suggestions using LLM
📈 Analytics Dashboard - Visualize progress with interactive charts
🔍 Smart Search - Find recordings by content, filename, or ID
🏷️ Status Filtering - Filter by completed, processing, or failed
✏️ Rename & Delete - Manage recordings with inline editing
📱 Responsive Design - Seamless experience on desktop and mobile

🔐 Security Features

JWT Authentication - Secure token-based auth
Password Hashing - Bcrypt encryption
CORS Protection - Configured for production
Rate Limiting - API abuse prevention
Input Validation - Pydantic schema validation
Admin Panel - Secure role-based access control

🎨 User Experience

Drag & Drop Upload - Intuitive file uploads
Real-time Updates - Auto-refresh processing status
Loading States - Clear feedback during operations
Error Handling - User-friendly error messages
Confirmation Modals - Prevent accidental deletions
Dark Mode Ready - (Coming Soon)


🎯 Why Commudio?
Problem
Public speaking anxiety affects 75% of people. Traditional speech coaching is:

⏰ Time-consuming - Requires scheduling sessions
💰 Expensive - $100-300 per session
📍 Location-dependent - In-person only

Solution
Commudio provides instant, AI-powered feedback at a fraction of the cost:

⚡ Instant Analysis - Get feedback in seconds
💵 Free to Use - No subscription required
🌍 Available 24/7 - Practice anytime, anywhere
📊 Track Progress - See improvement over time

Impact

"Commudio helped me reduce filler words by 60% in just 2 weeks!" - Beta User


🚀 Demo
Live Application
🔗 Frontend: commudio.vercel.app
🔗 API Docs: commudio-backend.onrender.com/docs
Test Credentials
Email: demo@commudio.com
Password: demo123

⚠️ Note: Demo account has limited features. Create your own account for full access.


🏗️ Tech Stack
Backend
Show Image
Show Image
Show Image

Framework: FastAPI (High-performance async API)
Database: PostgreSQL with SQLAlchemy ORM
Authentication: JWT with OAuth2
AI/ML: Groq API (Whisper for STT, LLaMA for feedback)
Validation: Pydantic
Testing: Pytest
Documentation: OpenAPI/Swagger

Frontend
Show Image
Show Image
Show Image

Framework: React 18 with Hooks
Build Tool: Vite (Fast HMR)
Styling: Tailwind CSS
Routing: React Router v6
HTTP Client: Axios
Charts: Recharts
Icons: Lucide React

DevOps
Show Image
Show Image
Show Image

Containerization: Docker & Docker Compose
Frontend Hosting: Vercel (Auto-deploy)
Backend Hosting: Render (PostgreSQL included)
CI/CD: GitHub Actions
Monitoring: Sentry (Error tracking)


📸 Screenshots
<details>
<summary>Click to expand screenshots</summary>
Login & Registration
Show Image
Show Image
Dashboard
Show Image
Upload & Analysis
Show Image
Show Image
Analytics
Show Image
Admin Panel
Show Image
</details>

🔧 Installation
Prerequisites
Ensure you have the following installed:
bash# Check versions
python --version   # 3.11+
node --version     # 18+
npm --version      # 9+
docker --version   # 24+ (optional)
Backend Setup
bash# 1. Clone the repository
git clone https://github.com/yourusername/commudio.git
cd commudio/backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your values (see Configuration section)

# 5. Initialize database
alembic upgrade head

# 6. Create admin user (optional)
python scripts/create_admin.py

# 7. Run development server
uvicorn app.main:app --reload

# Server runs on http://localhost:8000
# API docs: http://localhost:8000/docs
Frontend Setup
bash# 1. Navigate to frontend
cd ../frontend

# 2. Install dependencies
npm install

# 3. Set up environment variables
cp .env.example .env
# Edit .env with your API URL

# 4. Run development server
npm run dev

# Server runs on http://localhost:5173
Docker Setup
bash# 1. From project root
cd commudio

# 2. Build and run with Docker Compose
docker-compose up --build

# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
Stop containers:
bashdocker-compose down

⚙️ Configuration
Backend Environment Variables
Create .env in backend/ directory:
env# Database
DATABASE_URL=postgresql://user:password@localhost:5432/commudio
# For SQLite (development): sqlite:///./commudio.db

# Security
SECRET_KEY=your-super-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# API Keys
GROQ_API_KEY=gsk_your_groq_api_key_here

# CORS (update for production)
CORS_ORIGINS=http://localhost:5173,https://commudio.vercel.app
FRONTEND_URL=http://localhost:5173

# File Upload
MAX_FILE_SIZE_MB=25
ALLOWED_AUDIO_TYPES=.mp3,.wav,.m4a,.mp4

# Admin
ADMIN_EMAIL=admin@commudio.com
ADMIN_PASSWORD=secure_admin_password_change_me

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
Frontend Environment Variables
Create .env in frontend/ directory:
env# API URL
VITE_API_URL=http://localhost:8000
# For production: https://commudio-backend.onrender.com

# Environment
VITE_ENV=development

# Feature Flags
VITE_ENABLE_ANALYTICS=false
Generate Secret Key
bash# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -base64 32

🎯 Usage
1. Register an Account
bash# Via UI
1. Navigate to http://localhost:5173/register
2. Fill in email, username, password
3. Click "Create Account"

# Via API
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepass123"
  }'
2. Upload Audio Recording
bash# Via UI (recommended)
1. Login to dashboard
2. Navigate to Upload page
3. Drag & drop audio file or click to browse
4. Wait for processing (10-30 seconds)
5. View results on dashboard

# Via API
curl -X POST http://localhost:8000/recordings/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@recording.mp3"
3. View Analysis
Navigate to recording detail page to see:

Full transcript
Words per minute (WPM)
Filler word count
AI-generated feedback with improvement tips

4. Track Progress
Visit Analytics page to see:

Total recordings over time
Average WPM trend
Filler word reduction
Practice time statistics
