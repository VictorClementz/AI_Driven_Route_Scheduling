from geopy.distance import geodesic
from typing import Tuple

class DistanceService:

    AVERAGE_SPEED_KMH = 25 #Better solution might be needed but works rn

    @staticmethod
    def calculate_distance_km(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        return geodesic(point1, point2).kilometers

    @staticmethod
    def calculate_travel_time_hours(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        distance_km = DistanceService.calculate_distance_km(point1, point2)
        return distance_km / DistanceService.AVERAGE_SPEED_KMH

    @staticmethod
    def calculate_travel_time_minutes(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        return DistanceService.calculate_travel_time_hours(point1, point2) * 60