import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from api import staff_timetable

app = FastAPI(
    title="Agent Hub Staff Timetable API",
    version="1.0.0",
    docs_url="/staff-timetable/api/docs",
    redoc_url="/staff-timetable/api/redoc"
)

# CORS middleware for development
if os.getenv("ENVIRONMENT", "development") == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5174"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )

app.include_router(staff_timetable.router, prefix="/staff-timetable/api")


@app.get("/staff-timetable/api/health")
async def root():
    """API health check."""
    return {"message": "Agent Hub Staff Timetable API is running"}
