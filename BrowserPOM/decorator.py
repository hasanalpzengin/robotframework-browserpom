# ruff: noqa
def on_error_trigger(method):
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception:
            self.browser.keyword_error("body")
            raise

    return wrapper
