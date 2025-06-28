from datetime import datetime, time, timedelta
from typing import List, Optional, Tuple
from src.models.cleaner import Cleaner, Skill
from src.models.job import Job, Priority
from src.models.schedule import Assignment, DailySchedule, ScheduleOptimizationResult
from src.services.distance_service import DistanceService

class SimpleAssignmentService:

    #grabbed from gpt to test mvp before implementing OR-tools och VRPTW


    def __init__(self):
        self.distance_service = DistanceService()

    def create_schedule(self, cleaners: List[Cleaner], jobs: List[Job],
                        target_date: datetime) -> ScheduleOptimizationResult:
        """Create daily schedule using simple greedy algorithm"""

        schedules = []
        unassigned_jobs = []
        total_travel_time = 0.0

        # Sort jobs by priority and preferred start time
        sorted_jobs = sorted(jobs,
                             key=lambda j: (self._priority_weight(j.priority),
                                            j.preferred_start_time or time(12, 0)))

        for cleaner in cleaners:
            daily_schedule = self._create_cleaner_schedule(cleaner, sorted_jobs.copy(), target_date)
            schedules.append(daily_schedule)
            total_travel_time += daily_schedule.total_travel_hours

            # Remove assigned jobs from the list
            assigned_job_ids = [a.job_id for a in daily_schedule.assignments]
            sorted_jobs = [j for j in sorted_jobs if j.id not in assigned_job_ids]

        # Remaining jobs are unassigned
        unassigned_jobs = [j.id for j in sorted_jobs]

        # Simple optimization score (lower is better)
        optimization_score = total_travel_time + len(unassigned_jobs) * 2

        return ScheduleOptimizationResult(
            schedules=schedules,
            unassigned_jobs=unassigned_jobs,
            total_travel_time=total_travel_time,
            optimization_score=optimization_score,
            created_at=datetime.now()
        )

    def _create_cleaner_schedule(self, cleaner: Cleaner, available_jobs: List[Job],
                                 target_date: datetime) -> DailySchedule:
        """Create schedule for a single cleaner"""
        assignments = []
        current_time = cleaner.working_hours.start_time
        current_location = cleaner.home_coordinates
        total_work_hours = 0.0
        total_travel_hours = 0.0
        sequence_order = 0

        # Filter jobs that match cleaner's skills
        matching_jobs = [j for j in available_jobs
                         if self._has_required_skills(cleaner.skills, j.required_skills)]

        for job in matching_jobs:
            # Calculate travel time to job
            travel_time = self.distance_service.calculate_travel_time_hours(
                current_location, job.coordinates)

            # Calculate arrival time
            arrival_time = self._add_hours_to_time(current_time, travel_time)

            # Check if we can fit this job
            end_time = self._add_hours_to_time(arrival_time, job.estimated_duration_hours)

            # Check constraints
            if not self._can_assign_job(cleaner, job, arrival_time, end_time,
                                        total_work_hours + job.estimated_duration_hours,
                                        total_travel_hours + travel_time):
                continue

            # Calculate travel time from job (to next job or home)
            travel_from_job = 0.5  # Estimate, will be updated when we know next job

            # Create assignment
            assignment = Assignment(
                job_id=job.id,
                cleaner_id=cleaner.id,
                scheduled_start_time=arrival_time,
                scheduled_end_time=end_time,
                travel_time_to_job=travel_time,
                travel_time_from_job=travel_from_job,
                sequence_order=sequence_order
            )

            assignments.append(assignment)

            # Update state
            current_time = end_time
            current_location = job.coordinates
            total_work_hours += job.estimated_duration_hours
            total_travel_hours += travel_time
            sequence_order += 1

            # Remove job from available jobs
            available_jobs.remove(job)

        # Calculate travel time back home for last job
        if assignments:
            home_travel_time = self.distance_service.calculate_travel_time_hours(
                current_location, cleaner.home_coordinates)
            assignments[-1].travel_time_from_job = home_travel_time
            total_travel_hours += home_travel_time

        return DailySchedule(
            cleaner_id=cleaner.id,
            date=target_date,
            assignments=assignments,
            total_work_hours=total_work_hours,
            total_travel_hours=total_travel_hours,
            total_day_length=total_work_hours + total_travel_hours
        )

    def _has_required_skills(self, cleaner_skills: List[Skill],
                             required_skills: List[Skill]) -> bool:
        """Check if cleaner has all required skills"""
        return all(skill in cleaner_skills for skill in required_skills)

    def _can_assign_job(self, cleaner: Cleaner, job: Job, start_time: time,
                        end_time: time, total_work_hours: float,
                        total_travel_hours: float) -> bool:
        """Check if job can be assigned to cleaner"""

        # Check if job ends before cleaner's working hours end
        if end_time > cleaner.working_hours.end_time:
            return False

        # Check total day length constraint
        total_day_length = total_work_hours + total_travel_hours
        if total_day_length > cleaner.max_daily_hours:
            return False

        # Check if we can start after job's latest start time
        if job.latest_start_time and start_time > job.latest_start_time:
            return False

        return True

    def _add_hours_to_time(self, base_time: time, hours: float) -> time:
        """Add hours to a time object"""
        dt = datetime.combine(datetime.today(), base_time)
        dt += timedelta(hours=hours)
        return dt.time()

    def _priority_weight(self, priority: Priority) -> int:
        """Convert priority to numeric weight for sorting"""
        weights = {
            Priority.URGENT: 1,
            Priority.HIGH: 2,
            Priority.MEDIUM: 3,
            Priority.LOW: 4
        }
        return weights.get(priority, 3)