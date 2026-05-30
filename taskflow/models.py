from dataclasses import dataclass, field
from typing import Optional

from pydantic import BaseModel, Field

JOB_STATUSES = ("queued", "running", "done", "partial", "failed", "cancelled")


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
    status: str
    items: list
    processed: int = 0
    total: int = 0
    failed: list = field(default_factory=list)


class CreateJobBody(BaseModel):
    items: list = Field(default_factory=list)
