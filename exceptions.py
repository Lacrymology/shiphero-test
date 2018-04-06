class HttpError(Exception):
    status_code = 400

    def __init__(self, message='Bad Request', code=None, payload=None):
        super(Exception, self).__init__()
        self.message = message
        if code is not None:
            self.status_code = code
        self.payload = payload

    def to_dict(self):
        ret = dict(self.payload or ())
        ret['message'] = self.message
        return ret


class NotFoundError(HttpError):
    status_code = 404


class ForbiddenError(HttpError):
    status_code = 403
