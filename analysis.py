from typing import Dict


class Analyzer:
    """Calculates and aggregates real-time metrics from worker data."""
    
    def __init__(self):
        self.metrics = {'error_rate': 0, 'avg_response_time': 0, 'request_count': 0}

    def update_metrics(self, new_data: Dict) -> None:
        """Update real-time metrics with data from workers."""
        self.metrics['error_rate'] += new_data.get('error_rate', 0)
        self.metrics['avg_response_time'] += new_data.get('avg_response_time', 0)
        self.metrics['request_count'] += new_data.get('request_count', 0)

    def get_current_metrics(self) -> Dict:
        """Return the current aggregated metrics."""
        return self.metrics
