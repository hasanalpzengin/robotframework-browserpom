# https://mypy.readthedocs.io/en/stable/extending_mypy.html
from mypy.plugin import Plugin


class ChildObjectPlugin(Plugin):
    def get_function_hook(
        self, fullname
    ):
        if "ChildObject" in fullname:
            return self.transform_child_object
        return None

    def transform_child_object(self, ctx):
        filtered_type_context = [typ for typ in ctx.api.type_context if typ is not None]
        if filtered_type_context:
            return filtered_type_context[0]
        return ctx.default_return_type


def plugin(version):  # pylint: disable=unused-argument
    return ChildObjectPlugin
