from typing import List, Optional
from dataclasses import dataclass


@dataclass
class RewardModel:
    token_type_id: str
    count: int


@dataclass
class MilestoneModel:
    id: str
    reward_tickets: int
    icon: str
    reward: List[RewardModel]
