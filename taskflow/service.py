from taskflow import db, executor, pool
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
        total=0,
        ran_count=0,
        reserved=0,
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
    if not pool.reserve(pool.RESERVE):
        return None, 429, "no capacity"

    job.ran_count += 1
    job.reserved = pool.RESERVE
    results = {}
    total = 0
    for step in job.steps:
        ok = executor.run_step(step)
        results[step["id"]] = "succeeded" if ok else "failed"
        if ok:
            total += step.get("amount", 0)

    job.results = results
    job.total = total
    job.status = "done"
    if all(r == "succeeded" for r in results.values()):
        pool.release(pool.RESERVE)
    return job, 200, None


def cancel_job(job: Job):
    return {"id": job.id, "message": "cancelled"}
