from pydantic import BaseSettings

class Settings(BaseSettings):
    google_maps_api_key: str = ""
    lunch_duration_minutes: int = 30
    lunch_window_start: str = "11:30"
    lunch_window_end: str = "13:30"
    use_road_distances: bool = True

    class Config:
        env_file = ".env"

settings = Settings()