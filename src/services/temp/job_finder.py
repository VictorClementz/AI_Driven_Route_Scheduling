from typing import List, Optional, Tuple, Dict
from datetime import time
from src.models.cleaner import Cleaner
from src.models.job import Job
from src.services.distance_service import DistanceService
from .constraint_checker import ConstraintChecker

class JobFinder:
    def __init__(self, distance_service: DistanceService, constraint_checker: ConstraintChecker):
        self.distance_service = distance_service
        self.constraint_checker = constraint_checker

    def find_closest_job_to_location(self, jobs: List[Job], location: Tuple[float, float]) -> Optional[Job]:
        """Find the closest job to a given location"""
        if not jobs:
            return None

        closest_job = None
        min_distance = float('inf')

        for job in jobs:
            distance = self.distance_service.calculate_travel_time_hours(location, job.coordinates)
            if distance < min_distance:
                min_distance = distance
                closest_job = job

        return closest_job

    def find_closest_assignable_job(self, available_jobs: List[Job], current_location: Tuple[float, float],
                                    cleaner: Cleaner, current_time: time, total_work_hours: float,
                                    total_travel_hours: float) -> Optional[Job]:
        """Find the closest job that can still be assigned given constraints"""
        if not available_jobs or not current_location:
            return None

        # Filter jobs that match cleaner's skills
        matching_jobs = [j for j in available_jobs
                         if self.constraint_checker.has_required_skills(cleaner.skills, j.required_skills)]

        closest_job = None
        min_travel_time = float('inf')

        for job in matching_jobs:
            travel_time = self.distance_service.calculate_travel_time_hours(current_location, job.coordinates)
            arrival_time = self.constraint_checker._add_hours_to_time(current_time, travel_time)
            end_time = self.constraint_checker._add_hours_to_time(arrival_time, job.estimated_duration_hours)

            # Check if this job can be assigned
            if self.constraint_checker.can_assign_job(cleaner, job, arrival_time, end_time,
                                                      total_work_hours + job.estimated_duration_hours,
                                                      total_travel_hours + travel_time):
                if travel_time < min_travel_time:
                    min_travel_time = travel_time
                    closest_job = job

        return closest_job

    def find_best_next_job(self, available_jobs: List[Job], current_location: Tuple[float, float],
                           cleaner: Cleaner, current_time: time, total_work_hours: float,
                           total_travel_hours: float, job_clusters: Dict) -> Optional[Job]:
        """Find best next job considering clusters and constraints"""
        if not available_jobs or not current_location:
            return None

        # First, try to find jobs in the same cluster
        current_cluster = self._find_job_cluster(current_location, job_clusters)
        cluster_jobs = []

        if current_cluster:
            for job in available_jobs:
                if self._find_job_cluster(job.coordinates, job_clusters) == current_cluster:
                    cluster_jobs.append(job)

        # Search in cluster first, then all jobs
        for job_list in [cluster_jobs, available_jobs]:
            best_job = self.find_closest_assignable_job(
                job_list, current_location, cleaner, current_time,
                total_work_hours, total_travel_hours
            )
            if best_job:
                return best_job

        return None

    def _find_job_cluster(self, location: Tuple[float, float], job_clusters: Dict) -> Optional[Tuple[int, int]]:
        """Find which cluster a location belongs to"""
        for cluster_key, jobs in job_clusters.items():
            for job in jobs:
                if job.coordinates == location:
                    return cluster_key
        return None