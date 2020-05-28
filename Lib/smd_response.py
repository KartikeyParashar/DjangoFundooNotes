def SMD_Response(status=False, message="Something was wrong", data=[]):
    smd = {
        "status": status,
        "message": message,
        "data": data
    }
    return smd
