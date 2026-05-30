from taskflow import db, executor
from taskflow.models import Job, User


def create_job(owner: User, items):
    if not isinstance(items, list):
        return None, 400, "items must be a list"
    job = Job(
        id=db.new_id("job"),
        owner_id=owner.id,
        status="queued",
        items=items,
        processed=0,
        total=0,
        failed=[],
    )
    db.jobs[job.id] = job
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
    total = 0
    processed = 0
    failed = []
    for item in job.items:
        ok = executor.process_item(item)
        if not ok:
            failed.append(item.get("id"))
        total += item.get("amount", 0)
        processed += 1
    job.processed = processed
    job.total = total
    job.failed = failed
    job.status = "done"
    return job


def cancel_job(job: Job):
    return {"id": job.id, "message": "cancelled"}
