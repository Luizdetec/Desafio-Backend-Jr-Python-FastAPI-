from typing import Any

def success_response(data: Any):
    return {
        "success": True,
        "data": data
    }

def error_response(message: str, code: str = "BAD_REQUEST"):
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message
        }
    }