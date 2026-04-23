# ruff: noqa
from functools import wraps

def on_error_trigger(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception:
            self.browser.keyword_error("body")
            raise

    return wrapper
