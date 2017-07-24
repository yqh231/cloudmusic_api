from functools import wraps

from website.app.util import JsonError
def error(func):
    @wraps(func)
    def _wraps(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return JsonError(str(e))

    return _wraps

