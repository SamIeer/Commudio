from fastapi import FastAPI
from sqlalchemy import text
from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes import auth, users,recording

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:5432",
    settings.frontend_url,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(users.user)
app.include_router(recording.recording)

Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/db-test")
def db_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"db_response": result.scalar()}

