from datetime import time
from typing import List
from src.models.cleaner import Cleaner, Skill
from src.models.job import Job

class ConstraintChecker:
    def has_required_skills(self, cleaner_skills: List[Skill], required_skills: List[Skill]) -> bool:
        """Check if cleaner has all required skills"""
        return all(skill in cleaner_skills for skill in required_skills)

    def can_assign_first_job(self, cleaner: Cleaner, job: Job, start_time: time) -> bool:
        """Check if first job can be assigned (simpler check since no previous jobs)"""
        end_time = self._add_hours_to_time(start_time, job.estimated_duration_hours)

        # Check if job ends before cleaner's working hours end
        if end_time > cleaner.working_hours.end_time:
            return False

        # Check if job duration fits within max daily hours
        if job.estimated_duration_hours > cleaner.max_daily_hours:
            return False

        # Check if we can start after job's latest start time
        if job.latest_start_time and start_time > job.latest_start_time:
            return False

        return True

    def can_assign_job(self, cleaner: Cleaner, job: Job, start_time: time,
                       end_time: time, total_work_hours: float,
                       total_travel_hours: float) -> bool:
        """Check if job can be assigned to cleaner"""

        # Check if job ends before cleaner's working hours end
        if end_time > cleaner.working_hours.end_time:
            return False

        # Check total day length constraint (work + travel between jobs only)
        total_day_length = total_work_hours + total_travel_hours
        if total_day_length > cleaner.max_daily_hours:
            return False

        # Check if we can start after job's latest start time
        if job.latest_start_time and start_time > job.latest_start_time:
            return False

        return True

    def _add_hours_to_time(self, base_time: time, hours: float) -> time:
        """Add hours to a time object"""
        from datetime import datetime, timedelta
        dt = datetime.combine(datetime.today(), base_time)
        dt += timedelta(hours=hours)
        return dt.time()