from typing import List, Optional
from dataclasses import dataclass


@dataclass
class TaskStagesModel:
    count: int
    score: int


@dataclass
class TaskParamsModel:
    type: str
    param: str


@dataclass
class TaskModel:
    id: str
    task_type: str
    task_params: List[TaskParamsModel]
    task_stages: List[TaskStagesModel]
    text_loc_key: str
    icon: str
    map: Optional[list] = None
    map_groups: Optional[list] = None







