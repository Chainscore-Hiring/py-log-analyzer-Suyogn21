import os
import asyncio
import requests
from datetime import datetime
from typing import Dict
from log_entry import LogEntry

class Worker:
    """Handles processing of log file chunks and reporting results."""
    
    def __init__(self, worker_id: str, coordinator_url: str):
        self.worker_id = worker_id
        self.coordinator_url = coordinator_url

    async def process_chunk(self, filepath: str, start: int, size: int) -> Dict:
        """Process a chunk of the log file and return metrics."""
        metrics = {'error_rate': 0, 'avg_response_time': 0, 'request_count': 0}
        
        with open(filepath, 'r') as f:
            f.seek(start)
            chunk = f.read(size)
            for line in chunk.splitlines():
                log_entry = self.parse_log_line(line)
                if log_entry:
                    self.update_metrics(metrics, log_entry)
        
        await self.report_metrics(metrics)
        return metrics

    def parse_log_line(self, line: str):
        """Parse a single log line into a LogEntry."""
        try:
            timestamp, level, message = line.split(" ", 2)
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
            return LogEntry(timestamp, level, message)
        except Exception as e:
            return None

    def update_metrics(self, metrics: Dict, log_entry: LogEntry):
        """Update metrics based on log entry."""
        if log_entry.level == 'ERROR':
            metrics['error_rate'] += 1
        if 'ms' in log_entry.message:
            response_time = int(log_entry.message.split(" ")[-2].replace("ms", ""))
            metrics['avg_response_time'] += response_time
        metrics['request_count'] += 1

    async def report_metrics(self, metrics: Dict) -> None:
        """Send the metrics back to the coordinator."""
        response = requests.post(f"{self.coordinator_url}/report", json=metrics)
        if response.status_code != 200:
            print(f"Failed to report metrics: {response.text}")

    async def report_health(self) -> None:
        """Send heartbeat to coordinator to indicate worker status."""
        response = requests.post(f"{self.coordinator_url}/health", json={"worker_id": self.worker_id})
        if response.status_code != 200:
            print(f"Failed to send heartbeat: {response.text}")
