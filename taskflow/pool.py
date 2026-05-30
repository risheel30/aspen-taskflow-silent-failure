from taskflow import db

RESERVE = 2


def available():
    return db.pool["available"]


def reserve(n):
    if db.pool["available"] >= n:
        db.pool["available"] -= n
        return True
    return False


def release(n):
    db.pool["available"] = min(db.pool["available"] + n, db.POOL_CAPACITY)
