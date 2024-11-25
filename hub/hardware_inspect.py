import logging
from typing import Mapping
logger = logging.getLogger(__name__)

hpu_families = {}

class HWSystem:

    def __init__(self) -> None:
        self.total_hpu: Mapping = {}
        self.free_hpu: Mapping = {}
    
    def __str__(self) -> str:
        return f"Total HPU: {self.total_hpu}, Free HPU: {self.free_hpu}"

    def num_total_hpus(self) -> int:
        return 0
    
    def num_free_hpus(self) -> int:
        return 0

    def get_free_hpus(self) -> dict:
        return {}
    
class HPUUnit:
    """A single HPU device"""
    def __init__(self, name: str, device_index: int, device_id: str, total_memory: float, free_memory: float) -> None:
        self.name = name
        self.device_index = device_index
        self.device_id = device_id
        self.total_memory = total_memory
        self.device_index
        self.familay = None


def get_hardware_spec() -> HWSystem:
    """
    Get the hardware specification of the system.
    """
    system = HWSystem()
    return system