from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel, Field


@dataclass
class User:
    id: str
    email: str
    name: str
    role: str


@dataclass
class Job:
    id: str
    owner_id: str
    kind: str
    status: str
    payload: dict
    result: Optional[dict] = None


class CreateJobBody(BaseModel):
    kind: str
    payload: dict = Field(default_factory=dict)
