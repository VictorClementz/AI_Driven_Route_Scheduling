from typing import List, Dict, Tuple, Optional
from src.models.job import Job

class JobClusteringService:
    def cluster_jobs_by_area(self, jobs: List[Job], grid_size: int = 5) -> Dict[Tuple[int, int], List[Job]]:
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

    def find_job_cluster(self, location: Tuple[float, float], job_clusters: Dict) -> Optional[Tuple[int, int]]:
        """Find which cluster a location belongs to"""
        for cluster_key, jobs in job_clusters.items():
            for job in jobs:
                if job.coordinates == location:
                    return cluster_key
        return None