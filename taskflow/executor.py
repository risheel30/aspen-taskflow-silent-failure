from taskflow.models import Job

VALID_KINDS = ("export", "report", "crash")


def execute(job: Job) -> dict:
    if job.kind == "export":
        return {"ok": True, "output": f"exported {job.id}"}
    if job.kind == "report":
        return {"ok": False, "error": "downstream returned 500"}
    if job.kind == "crash":
        raise RuntimeError("executor crashed while running job")
    return {"ok": False, "error": "unknown kind"}
