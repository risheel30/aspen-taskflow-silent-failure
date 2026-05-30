import time


def run_step(step):
    time.sleep(0.01)
    amount = step.get("amount", 0)
    return isinstance(amount, (int, float)) and amount > 0
