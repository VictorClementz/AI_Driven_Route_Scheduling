from datetime import datetime, time
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

from src.models.cleaner import Skill



class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Job(BaseModel):
    id: str
    client_name: str
    address: str
    coordinates: tuple[float, float]
    required_skills: List[Skill]
    estimated_duration_hours: float
    preferred_start_time: Optional[time] = None
    preferred_end_time: Optional[time] = None
    latest_start_time: Optional[time] = None
    priority: Priority = Priority.MEDIUM
    instructions: Optional[str] = None
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            time: lambda v: v.isoformat() if v else None
        }