def process_item(item):
    amount = item.get("amount", 0)
    return isinstance(amount, (int, float)) and amount > 0
