class HttpResponse:
    def __init__(self, status_code: int, message: str, data: dict = None):
        self.status_code = status_code
        self.message = message
        self.data = data or {}

class HttpErrorResponse:
    def __init__(self, status_code: int, message: str, error_code: str = None):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"