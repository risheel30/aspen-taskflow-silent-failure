from taskflow import db, executor
from taskflow.models import Job, User


def create_job(owner: User, steps):
    ids = [s["id"] for s in steps]
    for s in steps:
        for dep in s.get("depends_on", []):
            if dep not in ids:
                return None, 400, "unknown dependency"
    job = Job(
        id=db.new_id("job"),
        owner_id=owner.id,
        status="queued",
        steps=steps,
        results={},
        ran_count=0,
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
    if job.status != "queued":
        return None, 409, "already run"

    job.ran_count += 1
    results = {}
    for step in job.steps:
        ok = executor.run_step(step)
        results[step["id"]] = "succeeded" if ok else "failed"

    job.results = results
    job.status = "done"
    return job, 200, None


def cancel_job(job: Job):
    return {"id": job.id, "message": "cancelled"}
