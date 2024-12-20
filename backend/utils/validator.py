def validate_request(data):
    if not data or "query" not in data:
        return False, "Invalid input: 'query' field is required."
    return True, None
