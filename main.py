from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import create_tables
from backend.config import settings
from backend.routers import users, predictions, analytics

app = FastAPI(
    title=settings.app_name,
    description="Prediction Confidence Decay Tracker API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(predictions.router)
app.include_router(analytics.router)

@app.on_event("startup")
def on_startup():
    create_tables()
    print(f"\n{settings.app_name} API is running!")
    print("Docs: http://localhost:8000/docs\n")

@app.get("/")
def root():
    return {
        "app": settings.app_name,
        "status": "running",
        "docs": "http://localhost:8000/docs"
    }