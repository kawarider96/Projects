from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from Domains.Task.Models.Task import Task

@dataclass
class Project:
    id: int
    parent_id: int | None
    name: str
    description: str | None
    start_date: date | None
    end_date: date | None

    level: int = 0
    children: list["Project"] = field(default_factory=list)
    tasks: list["Task"] = field(default_factory=list)