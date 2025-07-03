from typing import List
from src.models.schedule import DailySchedule
from src.models.job import Priority

class OptimizationScorer:
    def calculate_optimization_score(self, schedules: List[DailySchedule],
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

    def priority_weight(self, priority: Priority) -> int:
        """Convert priority to numeric weight for sorting"""
        weights = {
            Priority.URGENT: 1,
            Priority.HIGH: 2,
            Priority.MEDIUM: 3,
            Priority.LOW: 4
        }
        return weights.get(priority, 3)