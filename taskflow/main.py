from fastapi import FastAPI

from taskflow import db
from taskflow.api import jobs, pool

app = FastAPI(title="taskflow")
app.include_router(jobs.router)
app.include_router(pool.router)

db.seed()


@app.get("/")
def root():
    return {"service": "taskflow", "status": "ok"}
