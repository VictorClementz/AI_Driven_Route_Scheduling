from pydantic_settings import BaseSettings
from datetime import time

class Settings(BaseSettings):
    google_maps_api_key: str = ""
    lunch_duration_minutes: int = 30
    lunch_window_start: str = "11:30"
    lunch_window_end: str = "13:30"
    use_road_distances: bool = True
    clustering_grid_size: int = 5
    min_jobs_for_2opt: int = 4

    # Convert lunch duration to hours for compatibility
    @property
    def lunch_duration_hours(self) -> float:
        return self.lunch_duration_minutes / 60

    # Provide uppercase aliases for compatibility
    @property
    def CLUSTERING_GRID_SIZE(self) -> int:
        return self.clustering_grid_size

    @property
    def LUNCH_DURATION_HOURS(self) -> float:
        return self.lunch_duration_hours

    @property
    def LUNCH_WINDOW_START(self) -> time:
        hours, minutes = map(int, self.lunch_window_start.split(':'))
        return time(hours, minutes)

    @property
    def LUNCH_WINDOW_END(self) -> time:
        hours, minutes = map(int, self.lunch_window_end.split(':'))
        return time(hours, minutes)

    @property
    def MIN_JOBS_FOR_2OPT(self) -> int:
        return self.min_jobs_for_2opt

    class Config:
        env_file = ".env"

settings = Settings()