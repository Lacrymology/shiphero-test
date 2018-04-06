class HttpError(Exception):
    status_code=400

    def __init__(self, message='Bad Request', code=None):
        if code is not None:
            self.status_code = code
        self.message = message


class NotFoundError(HttpError):
    status_code=404
