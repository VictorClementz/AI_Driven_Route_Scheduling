from datetime import datetime
from typing import List
from src.models.schedule import Assignment, DailySchedule
from src.services.distance_service import DistanceService
from ...config import config

class RouteOptimizer:
    def __init__(self, distance_service: DistanceService, config: config = None):
        self.distance_service = distance_service
        self.config = config or config()

    def improve_schedules_2opt(self, schedules: List[DailySchedule],
                               target_date: datetime) -> List[DailySchedule]:
        """Simple 2-opt improvement to reduce travel time"""
        improved_schedules = []

        for schedule in schedules:
            if len(schedule.assignments) < self.config.MIN_JOBS_FOR_2OPT:
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
                        new_travel_time = self.calculate_total_travel_time(new_assignments)

                        if new_travel_time < best_travel_time:
                            best_assignments = new_assignments
                            best_travel_time = new_travel_time
                            improved = True
                            break
                    if improved:
                        break

            # Rebuild schedule with optimized sequence
            optimized_schedule = self.rebuild_schedule_with_new_sequence(
                schedule, best_assignments, target_date
            )
            improved_schedules.append(optimized_schedule)

        return improved_schedules

    def calculate_total_travel_time(self, assignments: List[Assignment]) -> float:
        """Calculate total travel time for a sequence of assignments"""
        return sum(a.travel_time_to_job for a in assignments)

    def rebuild_schedule_with_new_sequence(self, original_schedule: DailySchedule,
                                           new_assignments: List[Assignment],
                                           target_date: datetime) -> DailySchedule:
        """Rebuild schedule with new job sequence"""
        return DailySchedule(
            cleaner_id=original_schedule.cleaner_id,
            date=target_date,
            assignments=new_assignments,
            total_work_hours=original_schedule.total_work_hours,
            total_travel_hours=original_schedule.total_travel_hours,
            total_day_length=original_schedule.total_day_length
        )