from taskflow import db, executor
from taskflow.models import Job, User

MAX_ACTIVE = 2
ACTIVE_STATES = ("queued", "running")


def active_jobs(owner_id: str):
    return [j for j in db.jobs.values() if j.owner_id == owner_id and j.status in ACTIVE_STATES]


def create_job(owner: User, kind: str, payload: dict):
    if kind not in executor.VALID_KINDS:
        return None, 400, "invalid kind"

    job = Job(id=db.new_id("job"), owner_id=owner.id, kind=kind, status="queued", payload=payload)
    db.jobs[job.id] = job

    if len(active_jobs(owner.id)) > MAX_ACTIVE:
        return None, 429, "quota exceeded"

    return job, 200, None


def get_job(owner: User, job_id: str):
    job = db.jobs.get(job_id)
    if not job:
        return None, 404, "not found"
    if job.owner_id != owner.id and owner.role != "manager":
        return None, 404, "not found"
    return job, 200, None


def list_jobs(owner: User):
    return [j for j in db.jobs.values() if j.owner_id == owner.id]


def run_job(job: Job):
    job.status = "running"
    result = executor.execute(job)
    job.result = result
    job.status = "succeeded"
    return job


def cancel_job(job: Job):
    return {"id": job.id, "message": "cancelled"}
