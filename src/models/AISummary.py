from pydantic import BaseModel


class AISummary(BaseModel):
    task_name: str
    task_description: str
