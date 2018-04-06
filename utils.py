import functools

from flask import request

def authenticate(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # avoid possible import loops, since "utils" may grow into being used
        #  from most of the application
        from models import User
        request.user = User.get_dummy()
        return func(*args, **kwargs)
