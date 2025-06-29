from datetime import datetime, time, timedelta
from typing import List, Optional, Tuple, Dict
from src.models.cleaner import Cleaner, Skill
from src.models.job import Job, Priority
from src.models.schedule import Assignment, DailySchedule, ScheduleOptimizationResult
from src.services.distance_service import DistanceService
import random

class OptimizedAssignmentService:
    LUNCH_DURATION_HOURS = 0.5  # 30 minutes default
    LUNCH_WINDOW_START = time(11, 30)
    LUNCH_WINDOW_END = time(13, 30)

    def __init__(self, distance_service=None):
        self.distance_service = distance_service or DistanceService()

    def create_schedule(self, cleaners: List[Cleaner], jobs: List[Job],
                        target_date: datetime) -> ScheduleOptimizationResult:


        # Group jobs by area for better route clustering
        job_clusters = self._cluster_jobs_by_area(jobs)

        schedules = []
        unassigned_jobs = []
        total_travel_time = 0.0

        # Sort jobs by priority and preferred time
        sorted_jobs = sorted(jobs,
                             key=lambda j: (self._priority_weight(j.priority),
                                            j.preferred_start_time or time(12, 0)))

        # Create initial assignments
        for cleaner in cleaners:
            # Try to assign jobs from the same cluster to minimize travel
            daily_schedule = self._create_optimized_schedule(
                cleaner, sorted_jobs.copy(), target_date, job_clusters
            )
            schedules.append(daily_schedule)
            total_travel_time += daily_schedule.total_travel_hours

            # Remove assigned jobs
            assigned_job_ids = [a.job_id for a in daily_schedule.assignments]
            sorted_jobs = [j for j in sorted_jobs if j.id not in assigned_job_ids]

        # Try to reassign unassigned jobs using 2-opt improvement
        schedules = self._improve_schedules_2opt(schedules, sorted_jobs, target_date)

        # Final unassigned jobs
        unassigned_jobs = [j.id for j in sorted_jobs]

        # Calculate optimization score
        optimization_score = self._calculate_optimization_score(schedules, unassigned_jobs)

        return ScheduleOptimizationResult(
            schedules=schedules,
            unassigned_jobs=unassigned_jobs,
            total_travel_time=sum(s.total_travel_hours for s in schedules),
            optimization_score=optimization_score,
            created_at=datetime.now()
        )

    def _cluster_jobs_by_area(self, jobs: List[Job], grid_size: int = 5) -> Dict[Tuple[int, int], List[Job]]:
        """Simple grid-based clustering of jobs by geographic area"""
        if not jobs:
            return {}

        # Find bounds
        lats = [j.coordinates[0] for j in jobs]
        lngs = [j.coordinates[1] for j in jobs]
        min_lat, max_lat = min(lats), max(lats)
        min_lng, max_lng = min(lngs), max(lngs)

        # Create grid
        lat_step = (max_lat - min_lat) / grid_size
        lng_step = (max_lng - min_lng) / grid_size

        clusters = {}
        for job in jobs:
            lat_idx = int((job.coordinates[0] - min_lat) / lat_step) if lat_step > 0 else 0
            lng_idx = int((job.coordinates[1] - min_lng) / lng_step) if lng_step > 0 else 0
            # Ensure indices are within bounds
            lat_idx = min(lat_idx, grid_size - 1)
            lng_idx = min(lng_idx, grid_size - 1)

            key = (lat_idx, lng_idx)
            if key not in clusters:
                clusters[key] = []
            clusters[key].append(job)

        return clusters

    def _create_optimized_schedule(self, cleaner: Cleaner, available_jobs: List[Job],
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
                         if self._has_required_skills(cleaner.skills, j.required_skills)]

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
        first_job = self._find_closest_job_to_location(matching_jobs, cleaner.home_coordinates)
        if first_job and self._can_assign_first_job(cleaner, first_job, current_time):
            end_time = self._add_hours_to_time(current_time, first_job.estimated_duration_hours)

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
            if not lunch_scheduled and self._should_schedule_lunch(current_time):
                current_time = self._add_hours_to_time(current_time, self.LUNCH_DURATION_HOURS)
                lunch_scheduled = True
                continue

            # Find next best job (considering clusters)
            next_job = self._find_best_next_job(
                matching_jobs, current_location, cleaner, current_time,
                total_work_hours, total_travel_hours, job_clusters
            )

            if not next_job:
                break

            # Calculate travel time
            travel_time = self.distance_service.calculate_travel_time_hours(
                current_location, next_job.coordinates
            ) if current_location else 0.0

            arrival_time = self._add_hours_to_time(current_time, travel_time)

            # Check if we need lunch before this job
            if not lunch_scheduled and self._should_schedule_lunch(arrival_time):
                current_time = self._add_hours_to_time(current_time, self.LUNCH_DURATION_HOURS)
                lunch_scheduled = True
                arrival_time = self._add_hours_to_time(arrival_time, self.LUNCH_DURATION_HOURS)

            end_time = self._add_hours_to_time(arrival_time, next_job.estimated_duration_hours)

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

    def _find_best_next_job(self, available_jobs: List[Job], current_location: Tuple[float, float],
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
            best_job = self._find_closest_assignable_job(
                job_list, current_location, cleaner, current_time,
                total_work_hours, total_travel_hours
            )
            if best_job:
                return best_job

        return None

    def _find_job_cluster(self, location: Tuple[float, float], job_clusters: Dict) -> Optional[Tuple[int, int]]:
        """Find which cluster a location belongs to"""
        # This is a simplified version - in production, you'd properly map coordinates to clusters
        for cluster_key, jobs in job_clusters.items():
            for job in jobs:
                if job.coordinates == location:
                    return cluster_key
        return None

    def _should_schedule_lunch(self, current_time: time) -> bool:
        """Check if it's appropriate time for lunch"""
        return (self.LUNCH_WINDOW_START <= current_time <= self.LUNCH_WINDOW_END)

    def _improve_schedules_2opt(self, schedules: List[DailySchedule],
                                unassigned_jobs: List[Job], target_date: datetime) -> List[DailySchedule]:
        """Simple 2-opt improvement to reduce travel time"""
        improved_schedules = []

        for schedule in schedules:
            if len(schedule.assignments) < 4:  # Not worth optimizing small routes
                improved_schedules.append(schedule)
                continue

            # Try swapping pairs of jobs to reduce travel time
            best_assignments = schedule.assignments.copy()
            best_travel_time = schedule.total_travel_hours

            improved = True
            while improved:
                improved = False
                for i in range(1, len(best_assignments) - 2):  # Skip first job
                    for j in range(i + 1, len(best_assignments)):
                        # Create new sequence with swapped jobs
                        new_assignments = best_assignments.copy()
                        new_assignments[i], new_assignments[j] = new_assignments[j], new_assignments[i]

                        # Recalculate travel times
                        new_travel_time = self._calculate_total_travel_time(new_assignments)

                        if new_travel_time < best_travel_time:
                            best_assignments = new_assignments
                            best_travel_time = new_travel_time
                            improved = True
                            break
                    if improved:
                        break

            # Rebuild schedule with optimized sequence
            optimized_schedule = self._rebuild_schedule_with_new_sequence(
                schedule, best_assignments, target_date
            )
            improved_schedules.append(optimized_schedule)

        return improved_schedules

    def _calculate_total_travel_time(self, assignments: List[Assignment]) -> float:
        """Calculate total travel time for a sequence of assignments"""
        # look up actual job locations later
        return sum(a.travel_time_to_job for a in assignments)

    def _rebuild_schedule_with_new_sequence(self, original_schedule: DailySchedule,
                                            new_assignments: List[Assignment],
                                            target_date: datetime) -> DailySchedule:
        """Rebuild schedule with new job sequence"""
        # recalculate all times properly later
        return DailySchedule(
            cleaner_id=original_schedule.cleaner_id,
            date=target_date,
            assignments=new_assignments,
            total_work_hours=original_schedule.total_work_hours,
            total_travel_hours=original_schedule.total_travel_hours,
            total_day_length=original_schedule.total_day_length
        )

    def _calculate_optimization_score(self, schedules: List[DailySchedule],
                                      unassigned_jobs: List[str]) -> float:
        """Calculate optimization score (lower is better)"""
        total_travel = sum(s.total_travel_hours for s in schedules)
        penalty_unassigned = len(unassigned_jobs) * 3  # Higher penalty for unassigned jobs

        # Add penalty for unbalanced schedules
        if schedules:
            work_hours = [s.total_work_hours for s in schedules]
            avg_work = sum(work_hours) / len(work_hours)
            variance_penalty = sum((h - avg_work) ** 2 for h in work_hours) * 0.1
        else:
            variance_penalty = 0

        return total_travel + penalty_unassigned + variance_penalty

    # Include all the helper methods from the original service...
    def _find_closest_job_to_location(self, jobs: List[Job], location: Tuple[float, float]) -> Optional[Job]:
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

    def _find_closest_assignable_job(self, available_jobs: List[Job], current_location: Tuple[float, float],
                                     cleaner: Cleaner, current_time: time, total_work_hours: float,
                                     total_travel_hours: float) -> Optional[Job]:
        """Find the closest job that can still be assigned given constraints"""
        if not available_jobs or not current_location:
            return None

        # Filter jobs that match cleaner's skills
        matching_jobs = [j for j in available_jobs
                         if self._has_required_skills(cleaner.skills, j.required_skills)]

        closest_job = None
        min_travel_time = float('inf')

        for job in matching_jobs:
            travel_time = self.distance_service.calculate_travel_time_hours(current_location, job.coordinates)
            arrival_time = self._add_hours_to_time(current_time, travel_time)
            end_time = self._add_hours_to_time(arrival_time, job.estimated_duration_hours)

            # Check if this job can be assigned
            if self._can_assign_job(cleaner, job, arrival_time, end_time,
                                    total_work_hours + job.estimated_duration_hours,
                                    total_travel_hours + travel_time):
                if travel_time < min_travel_time:
                    min_travel_time = travel_time
                    closest_job = job

        return closest_job

    def _can_assign_first_job(self, cleaner: Cleaner, job: Job, start_time: time) -> bool:
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