from typing import List, Optional
from pydantic import BaseModel
from datetime import time
from enum import Enum

class Skill(str, Enum):
    OFFICE_CLEANING = "office_cleaning"
    WINDOW_CLEANING = "window_cleaning"
    APARTMENT_CLEANING = "apartment_cleaning"
    OUTDOOR_CLEANING = "outdoor_cleaning"
    SNOW_SHOWELING = "snow_showeling"
    HOME_CLEANING = "home_cleaning"

class WorkingHours(BaseModel):
    start_time: time
    end_time: time

class Cleaner(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    home_address: str
    home_coordinates: tuple[float, float]
    skills: List[Skill]
    languages: list[str] = [] #Fixa sen
    working_hours: WorkingHours
    max_daily_hours: float = 8.0
    hourly_rate: Optional[float] = None

    class Config:
        json_encoders = {
            time: lambda v: v.isoformat()
        }