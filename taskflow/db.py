from taskflow.models import User

POOL_CAPACITY = 3

users: dict = {}
tokens: dict = {}
jobs: dict = {}
pool: dict = {"available": POOL_CAPACITY}

_counter = {"n": 0}


def new_id(prefix: str) -> str:
    _counter["n"] += 1
    return f"{prefix}-{_counter['n']:04d}"


def seed():
    users.clear()
    tokens.clear()
    jobs.clear()
    pool["available"] = POOL_CAPACITY
    _counter["n"] = 0

    cast = [
        User(id="user-risheel", email="risheel@example.com", name="Risheel", role="member"),
        User(id="user-vaibhav", email="vaibhav@example.com", name="Vaibhav", role="member"),
        User(id="user-manthan", email="manthan@example.com", name="Manthan", role="member"),
        User(id="user-priya", email="priya@example.com", name="Priya", role="manager"),
    ]
    for u in cast:
        users[u.id] = u
        tokens[f"tok-{u.name.lower()}"] = u.id
