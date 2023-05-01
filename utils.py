def find_key_value(data, target_key):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            found_value = find_key_value(value, target_key)
            if found_value is not None:
                return found_value
    elif isinstance(data, list):
        for item in data:
            found_value = find_key_value(item, target_key)
            if found_value is not None:
                return found_value
    return None