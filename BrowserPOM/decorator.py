def on_error_trigger(method):
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception as e:
            self.browser.keyword_error("body")
            raise
    return wrapper