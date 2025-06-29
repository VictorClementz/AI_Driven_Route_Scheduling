from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime

from ..models.cleaner import Cleaner
from ..models.job import Job
from ..models.schedule import ScheduleOptimizationResult
from ..services.assignment_service import OptimizedAssignmentService
from ..data.dummy import DummyDataGenerator
from ..services.distance_service import DistanceService
from ..services.road_distance_service import RoadDistanceService
import os


GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # Set this in your .env file
if GOOGLE_MAPS_API_KEY:
    distance_service = RoadDistanceService(GOOGLE_MAPS_API_KEY)
else:
    distance_service = DistanceService()  # Fallback to geodesic

assignment_service = OptimizedAssignmentService(distance_service)
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ska byta till postgres eller nått senare
cleaners_db = DummyDataGenerator.create_cleaners()
jobs_db = DummyDataGenerator.create_jobs()
#assignment_service = SimpleAssignmentService()

@app.get("/api/cleaners", response_model=List[Cleaner])
async def get_cleaners():
    """Hämta alla städare"""
    return cleaners_db

@app.get("/api/cleaners/{cleaner_id}", response_model=Cleaner)
async def get_cleaner(cleaner_id: str):
    """Hämta en specifik städare"""
    cleaner = next((c for c in cleaners_db if c.id == cleaner_id), None)
    if not cleaner:
        raise HTTPException(status_code=404, detail="Cleaner not found")
    return cleaner

@app.get("/api/jobs", response_model=List[Job])
async def get_jobs():
    """Hämta alla jobb"""
    return jobs_db

@app.get("/api/jobs/{job_id}", response_model=Job)
async def get_job(job_id: str):
    """Hämta ett specifikt jobb"""
    job = next((j for j in jobs_db if j.id == job_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/api/schedules/today", response_model=ScheduleOptimizationResult)
async def get_today_schedule():
    """Hämta dagens schema"""
    target_date = datetime.now()
    result = assignment_service.create_schedule(cleaners_db, jobs_db, target_date)
    return result

@app.post("/api/schedules/generate", response_model=ScheduleOptimizationResult)
async def generate_schedule(date: datetime = None):
    """Generera nytt schema för specifikt datum"""
    if not date:
        date = datetime.now()
    result = assignment_service.create_schedule(cleaners_db, jobs_db, date)
    return result