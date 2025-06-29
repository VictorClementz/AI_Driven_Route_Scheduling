import googlemaps
from datetime import datetime
from typing import Tuple, Optional
from .distance_service import DistanceService

class RoadDistanceService(DistanceService):
    def __init__(self, api_key: str):
        self.gmaps = googlemaps.Client(key=api_key)
        self._cache = {}

    def calculate_distance_km(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        distance_km, _ = self._get_distance_and_time(point1, point2)
        return distance_km

    def calculate_travel_time_hours(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        _, duration_hours = self._get_distance_and_time(point1, point2)
        return duration_hours

    def _get_distance_and_time(self, origin: Tuple[float, float],
                               destination: Tuple[float, float]) -> Tuple[float, float]:
        cache_key = f"{origin}_{destination}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            result = self.gmaps.distance_matrix(
                origins=[origin],
                destinations=[destination],
                mode="driving",
                departure_time=datetime.now()
            )

            if result['rows'][0]['elements'][0]['status'] == 'OK':
                distance_km = result['rows'][0]['elements'][0]['distance']['value'] / 1000
                duration_hours = result['rows'][0]['elements'][0]['duration']['value'] / 3600
                self._cache[cache_key] = (distance_km, duration_hours)
                return distance_km, duration_hours
        except Exception as e:
            print(f"Google Maps API error: {e}")


        distance_km = super().calculate_distance_km(origin, destination)
        duration_hours = super().calculate_travel_time_hours(origin, destination)
        return distance_km, duration_hours