from fastapi import APIRouter, Depends

from taskflow import db
from taskflow.auth import current_user

router = APIRouter(prefix="/pool", tags=["pool"])


@router.get("")
def read_pool(user=Depends(current_user)):
    return {"capacity": db.POOL_CAPACITY, "available": db.pool["available"]}
