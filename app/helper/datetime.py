def serialize_datetime(value):
    return value.isoformat() if value else None