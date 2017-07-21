from pymongo.errors import DuplicateKeyError
from functools import wraps


def error(func):
    @wraps(func)
    def _wraps(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            pass

    return _wraps
