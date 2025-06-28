from datetime import datetime, time
from typing import List, Optional
from pydantic import BaseModel

class Assignment(BaseModel):
    job_id: str
    cleaner_id: str
    scheduled_start_time: time
    scheduled_end_time: time
    travel_time_to_job: float
    travel_time_from_job: float
    sequence_order: int

class DailySchedule(BaseModel):
    cleaner_id: str
    date: datetime
    assignments: List[Assignment]
    total_work_hours: float
    total_travel_hours: float
    total_day_length: float  

    def is_valid(self, max_day_length: float = 9.0) -> bool:
        return self.total_day_length <= max_day_length

class ScheduleOptimizationResult(BaseModel):
    schedules: List[DailySchedule]
    unassigned_jobs: List[str]
    total_travel_time: float
    optimization_score: float
    created_at: datetime