
from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    id: int
    project_id: int
    name: str | None
    description: str | None
    start_date: date | None
    end_date: date | None