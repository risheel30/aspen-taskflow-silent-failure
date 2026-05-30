from dataclasses import dataclass, field

from pydantic import BaseModel, Field

JOB_STATUSES = ("queued", "running", "done", "failed", "cancelled")
STEP_STATUSES = ("pending", "succeeded", "failed", "skipped")


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
    steps: list
    results: dict = field(default_factory=dict)
    total: int = 0
    ran_count: int = 0


class Step(BaseModel):
    id: str
    amount: float = 0
    depends_on: list = Field(default_factory=list)


class CreateJobBody(BaseModel):
    steps: list[Step] = Field(default_factory=list)
