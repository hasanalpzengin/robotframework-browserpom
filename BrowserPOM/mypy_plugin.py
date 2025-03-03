# https://mypy.readthedocs.io/en/stable/extending_mypy.html
from mypy.plugin import Plugin


class ChildObjectPlugin(Plugin):
    """
    A custom mypy plugin to handle the ChildObject class.

    Methods:
        get_function_hook(fullname):
            Returns a function hook for the ChildObject class if found in the fully qualified name.

        transform_child_object(ctx):
            Transforms the ChildObject type based on the type context provided by mypy.
    """

    def get_function_hook(self, fullname):
        """
        Returns a function hook for the ChildObject class.

        Args:
            fullname (str): The fully qualified name of the function.

        Returns:
            function: The transform_child_object function if "ChildObject" is found in the fullname, otherwise None.
        """
        if "ChildObject" in fullname:
            return self.transform_child_object
        return None

    def transform_child_object(self, ctx):
        """
        Transforms the ChildObject type based on the type context.

        Args:
            ctx: The context provided by mypy.

        Returns:
            Type: The first non-None type in the type context, or the default return type if none are found.
        """
        filtered_type_context = [typ for typ in ctx.api.type_context if typ is not None]
        if filtered_type_context:
            return filtered_type_context[0]
        return ctx.default_return_type


def plugin(version):  # pylint: disable=unused-argument
    """
    Returns an instance of the ChildObjectPlugin.

    Args:
        version (str): The mypy version (unused).

    Returns:
        ChildObjectPlugin: An instance of the ChildObjectPlugin.
    """
    return ChildObjectPlugin
