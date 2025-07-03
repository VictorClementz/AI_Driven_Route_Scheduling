from datetime import time
from ...config import config

class LunchScheduler:
    def __init__(self, config: config):
        self.config = config

    def should_schedule_lunch(self, current_time: time) -> bool:
        """Check if it's appropriate time for lunch"""
        return (self.config.LUNCH_WINDOW_START <= current_time <= self.config.LUNCH_WINDOW_END)