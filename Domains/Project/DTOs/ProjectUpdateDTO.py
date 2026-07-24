from datetime import date

from pydantic import BaseModel


class ProjectUpdateDTO(BaseModel):
    parent_id: int | None = None
    name: str | None = None
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None