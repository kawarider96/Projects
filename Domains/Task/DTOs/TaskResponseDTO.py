from datetime import date

from pydantic import BaseModel, ConfigDict


class TaskResponseDTO(BaseModel):
    id: int
    project_id: int
    name: str
    description: str | None
    start_date: date | None
    end_date: date | None

    model_config = ConfigDict(
        from_attributes=True
    )