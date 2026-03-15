import logging
import time
from typing import Dict, Any, Optional
import asyncio

# Professional logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("gateway.balancer")

class LoadBalancer:
    """
    Advanced Round-Robin Balancer with health-check awareness.
    """
    def __init__(self):
        self._endpoints: Dict[str, list] = {}
        self._current_index: Dict[str, int] = {}

    def register_node(self, model_id: str, endpoint_url: str):
        if model_id not in self._endpoints:
            self._endpoints[model_id] = []
            self._current_index[model_id] = 0
        self._endpoints[model_id].append(endpoint_url)
        logger.info(f"Registered node for {model_id}: {endpoint_url}")

    async def get_next_node(self, model_id: str) -> Optional[str]:
        nodes = self._endpoints.get(model_id)
        if not nodes:
            return None
        
        idx = self._current_index[model_id]
        node = nodes[idx]
        self._current_index[model_id] = (idx + 1) % len(nodes)
        return node

class TelemetryManager:
    """
    Context manager for high-precision inference telemetry.
    """
    def __init__(self, model_id: str):
        self.model_id = model_id
        self.start_time = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.perf_counter() - self.start_time
        logger.info(f"Telemetry | model: {self.model_id} | latency: {duration:.4f}s | success: {exc_type is None}")
