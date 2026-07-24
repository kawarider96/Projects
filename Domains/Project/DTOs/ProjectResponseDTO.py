from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict

from Domains.Task.DTOs.TaskResponseDTO import TaskResponseDTO


class ProjectResponseDTO(BaseModel):
    id: int
    parent_id: int | None
    name: str
    description: str | None
    start_date: date | None
    end_date: date | None
    level: int

    tasks: list[TaskResponseDTO]
    children: list["ProjectResponseDTO"]

    model_config = ConfigDict(
        from_attributes=True
    )