def run_step(step):
    amount = step.get("amount", 0)
    return isinstance(amount, (int, float)) and amount > 0
