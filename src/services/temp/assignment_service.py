from datetime import datetime, time
from typing import List
from src.models.cleaner import Cleaner
from src.models.job import Job
from src.models.schedule import ScheduleOptimizationResult
from src.services.distance_service import DistanceService
from .job_clustering import JobClusteringService
from .schedule_builder import ScheduleBuilder
from .route_optimizer import RouteOptimizer
from .optimization_scorer import OptimizationScorer
from src.config import config
from ...config.config import settings


class OptimizedAssignmentService:
    def __init__(self, distance_service=None, config: config = None):
        self.distance_service = distance_service or DistanceService()
        self.config = config or settings

        # Initialize all sub-services
        self.clustering_service = JobClusteringService()
        self.schedule_builder = ScheduleBuilder(self.distance_service, self.config)
        self.route_optimizer = RouteOptimizer(self.distance_service, self.config)
        self.scorer = OptimizationScorer()

    def create_schedule(self, cleaners: List[Cleaner], jobs: List[Job],
                        target_date: datetime) -> ScheduleOptimizationResult:
        # Group jobs by area for better route clustering
        job_clusters = self.clustering_service.cluster_jobs_by_area(
            jobs, self.config.CLUSTERING_GRID_SIZE
        )

        schedules = []
        total_travel_time = 0.0

        # Sort jobs by priority and preferred time
        sorted_jobs = sorted(jobs,
                             key=lambda j: (self.scorer.priority_weight(j.priority),
                                            j.preferred_start_time or time(12, 0)))

        # Create initial assignments
        for cleaner in cleaners:
            daily_schedule = self.schedule_builder.create_optimized_schedule(
                cleaner, sorted_jobs.copy(), target_date, job_clusters
            )
            schedules.append(daily_schedule)
            total_travel_time += daily_schedule.total_travel_hours

            # Remove assigned jobs
            assigned_job_ids = [a.job_id for a in daily_schedule.assignments]
            sorted_jobs = [j for j in sorted_jobs if j.id not in assigned_job_ids]

        # Try to reassign unassigned jobs using 2-opt improvement
        optimized_schedules = self.route_optimizer.improve_schedules_2opt(schedules, target_date)

        # Final unassigned jobs
        unassigned_jobs = [j.id for j in sorted_jobs]

        # Calculate optimization score
        optimization_score = self.scorer.calculate_optimization_score(
            optimized_schedules, unassigned_jobs
        )

        return ScheduleOptimizationResult(
            schedules=optimized_schedules,
            unassigned_jobs=unassigned_jobs,
            total_travel_time=sum(s.total_travel_hours for s in optimized_schedules),
            optimization_score=optimization_score,
            created_at=datetime.now()
        )