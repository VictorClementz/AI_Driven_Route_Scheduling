from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from typing import List
from datetime import datetime, date
import uvicorn

from src.models.cleaner import Cleaner
from src.models.job import Job
from src.models.schedule import ScheduleOptimizationResult
from src.services.assignment_service import SimpleAssignmentService
from src.data.dummy import DummyDataGenerator

app = FastAPI(title="Cleaning Scheduler API", version="0.1.0")

# In-memory storage for MVP
cleaners_db: List[Cleaner] = []
jobs_db: List[Job] = []
assignment_service = SimpleAssignmentService()

@app.on_event("startup")
async def startup_event():
    """Load dummy data on startup"""
    global cleaners_db, jobs_db
    cleaners_db = DummyDataGenerator.create_cleaners()
    jobs_db = DummyDataGenerator.create_jobs()
    print(f"Loaded {len(cleaners_db)} cleaners and {len(jobs_db)} jobs")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head><title>Cleaning Scheduler</title></head>
        <body>
            <h1>Cleaning Scheduler API</h1>
            <p>Welcome to the Cleaning Scheduler MVP!</p>
            <ul>
                <li><a href="/docs">API Documentation (Swagger)</a></li>
                <li><a href="/cleaners">View Cleaners</a></li>
                <li><a href="/jobs">View Jobs</a></li>
                <li><a href="/schedule/today">Generate Today's Schedule</a></li>
            </ul>
        </body>
    </html>
    """

@app.get("/cleaners", response_model=List[Cleaner])
async def get_cleaners():
    """Get all cleaners"""
    return cleaners_db

@app.get("/jobs", response_model=List[Job])
async def get_jobs():
    """Get all jobs"""
    return jobs_db

@app.post("/cleaners", response_model=Cleaner)
async def create_cleaner(cleaner: Cleaner):
    """Create a new cleaner"""
    cleaners_db.append(cleaner)
    return cleaner

@app.post("/jobs", response_model=Job)
async def create_job(job: Job):
    """Create a new job"""
    jobs_db.append(job)
    return job

@app.get("/schedule/today", response_model=ScheduleOptimizationResult)
async def generate_todays_schedule():
    """Generate schedule for today"""
    if not cleaners_db or not jobs_db:
        raise HTTPException(status_code=400, detail="No cleaners or jobs available")

    result = assignment_service.create_schedule(
        cleaners=cleaners_db,
        jobs=jobs_db,
        target_date=datetime.now()
    )
    return result

@app.get("/schedule/{date_str}", response_model=ScheduleOptimizationResult)
async def generate_schedule_for_date(date_str: str):
    """Generate schedule for specific date (YYYY-MM-DD)"""
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    if not cleaners_db or not jobs_db:
        raise HTTPException(status_code=400, detail="No cleaners or jobs available")

    result = assignment_service.create_schedule(
        cleaners=cleaners_db,
        jobs=jobs_db,
        target_date=target_date
    )
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)