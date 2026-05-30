from fastapi import Header, HTTPException

from taskflow import db


def current_user(authorization: str = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="missing authorization")
    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="bad authorization")
    token = parts[1]
    user_id = db.tokens.get(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="unknown token")
    return db.users[user_id]
