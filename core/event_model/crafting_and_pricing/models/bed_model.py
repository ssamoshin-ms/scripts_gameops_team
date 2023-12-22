from typing import List, Optional
from dataclasses import dataclass


@dataclass
class BedModel:
    item_id: str
    item_amount_pickup: int
    chopping_cost: int
    time: int
    skip: str
    