from fastapi import APIRouter, Depends, HTTPException

from taskflow import service
from taskflow.auth import current_user
from taskflow.models import CreateJobBody

router = APIRouter(prefix="/jobs", tags=["jobs"])


def _serialize(job):
    return {
        "id": job.id,
        "owner_id": job.owner_id,
        "status": job.status,
        "steps": job.steps,
        "results": job.results,
        "total": job.total,
        "ran_count": job.ran_count,
    }


@router.post("")
def create(body: CreateJobBody, user=Depends(current_user)):
    steps = [s.model_dump() for s in body.steps]
    job, code, err = service.create_job(user, steps)
    if err:
        raise HTTPException(status_code=code, detail=err)
    return _serialize(job)


@router.get("")
def list_mine(user=Depends(current_user)):
    return [_serialize(j) for j in service.list_jobs(user)]


@router.get("/{job_id}")
def read(job_id: str, user=Depends(current_user)):
    job, code, err = service.get_job(user, job_id)
    if err:
        raise HTTPException(status_code=code, detail=err)
    return _serialize(job)


@router.post("/{job_id}/run")
def run(job_id: str, user=Depends(current_user)):
    job, code, err = service.get_job(user, job_id)
    if err:
        raise HTTPException(status_code=code, detail=err)
    job, code, err = service.run_job(job)
    if err:
        raise HTTPException(status_code=code, detail=err)
    return _serialize(job)


@router.post("/{job_id}/cancel")
def cancel(job_id: str, user=Depends(current_user)):
    job, code, err = service.get_job(user, job_id)
    if err:
        raise HTTPException(status_code=code, detail=err)
    return service.cancel_job(job)
