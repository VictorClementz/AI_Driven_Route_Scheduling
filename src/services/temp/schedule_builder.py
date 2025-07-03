from datetime import datetime, time
from typing import List, Dict
from src.models.cleaner import Cleaner
from src.models.job import Job
from src.models.schedule import Assignment, DailySchedule
from src.services.distance_service import DistanceService
from .constraint_checker import ConstraintChecker
from .job_finder import JobFinder
from .lunch_scheduler import LunchScheduler
from ...config import config

class ScheduleBuilder:
    def __init__(self, distance_service: DistanceService, config: config = None):
        self.distance_service = distance_service
        self.config = config or config()
        self.constraint_checker = ConstraintChecker()
        self.job_finder = JobFinder(distance_service, self.constraint_checker)
        self.lunch_scheduler = LunchScheduler(self.config)

    def create_optimized_schedule(self, cleaner: Cleaner, available_jobs: List[Job],
                                  target_date: datetime, job_clusters: Dict) -> DailySchedule:
        """Create schedule with lunch break and clustered job assignment"""
        assignments = []
        current_time = cleaner.working_hours.start_time
        current_location = None
        total_work_hours = 0.0
        total_travel_hours = 0.0
        sequence_order = 0
        lunch_scheduled = False

        # Filter jobs by skills
        matching_jobs = [j for j in available_jobs
                         if self.constraint_checker.has_required_skills(cleaner.skills, j.required_skills)]

        if not matching_jobs:
            return DailySchedule(
                cleaner_id=cleaner.id,
                date=target_date,
                assignments=[],
                total_work_hours=0,
                total_travel_hours=0,
                total_day_length=0
            )

        # Start with job closest to home
        first_job = self.job_finder.find_closest_job_to_location(matching_jobs, cleaner.home_coordinates)
        if first_job and self.constraint_checker.can_assign_first_job(cleaner, first_job, current_time):
            end_time = self.constraint_checker._add_hours_to_time(current_time, first_job.estimated_duration_hours)

            assignments.append(Assignment(
                job_id=first_job.id,
                cleaner_id=cleaner.id,
                scheduled_start_time=current_time,
                scheduled_end_time=end_time,
                travel_time_to_job=0.0,
                travel_time_from_job=0.0,
                sequence_order=sequence_order
            ))

            current_time = end_time
            current_location = first_job.coordinates
            total_work_hours += first_job.estimated_duration_hours
            sequence_order += 1
            matching_jobs.remove(first_job)

        # Continue assigning jobs with lunch break consideration
        while matching_jobs and current_time < cleaner.working_hours.end_time:
            # Check if it's time for lunch
            if not lunch_scheduled and self.lunch_scheduler.should_schedule_lunch(current_time):
                current_time = self.constraint_checker._add_hours_to_time(current_time, self.config.LUNCH_DURATION_HOURS)
                lunch_scheduled = True
                continue

            # Find next best job (considering clusters)
            next_job = self.job_finder.find_best_next_job(
                matching_jobs, current_location, cleaner, current_time,
                total_work_hours, total_travel_hours, job_clusters
            )

            if not next_job:
                break

            # Calculate travel time
            travel_time = self.distance_service.calculate_travel_time_hours(
                current_location, next_job.coordinates
            ) if current_location else 0.0

            arrival_time = self.constraint_checker._add_hours_to_time(current_time, travel_time)

            # Check if we need lunch before this job
            if not lunch_scheduled and self.lunch_scheduler.should_schedule_lunch(arrival_time):
                current_time = self.constraint_checker._add_hours_to_time(current_time, self.config.LUNCH_DURATION_HOURS)
                lunch_scheduled = True
                arrival_time = self.constraint_checker._add_hours_to_time(arrival_time, self.config.LUNCH_DURATION_HOURS)

            end_time = self.constraint_checker._add_hours_to_time(arrival_time, next_job.estimated_duration_hours)

            # Create assignment
            assignment = Assignment(
                job_id=next_job.id,
                cleaner_id=cleaner.id,
                scheduled_start_time=arrival_time,
                scheduled_end_time=end_time,
                travel_time_to_job=travel_time,
                travel_time_from_job=0.0,
                sequence_order=sequence_order
            )

            assignments.append(assignment)

            # Update previous assignment's travel_time_from_job
            if len(assignments) > 1:
                assignments[-2].travel_time_from_job = travel_time

            # Update state
            current_time = end_time
            current_location = next_job.coordinates
            total_work_hours += next_job.estimated_duration_hours
            total_travel_hours += travel_time
            sequence_order += 1
            matching_jobs.remove(next_job)

        return DailySchedule(
            cleaner_id=cleaner.id,
            date=target_date,
            assignments=assignments,
            total_work_hours=total_work_hours,
            total_travel_hours=total_travel_hours,
            total_day_length=total_work_hours + total_travel_hours
        )