from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ChopModel:
    item_id: str
    item_amount_pickup: int
    chopping_cost: int

