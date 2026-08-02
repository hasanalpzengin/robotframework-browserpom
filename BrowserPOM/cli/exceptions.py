"""Domain-specific exceptions for the browserpom CLI."""


class BrowserPOMCLIError(Exception):
    """Base class for all browserpom CLI errors."""


class ConfigError(BrowserPOMCLIError):
    """Raised when [tool.browserpom.discover] configuration is invalid."""


class DiscoveryError(BrowserPOMCLIError):
    """Raised when AST-based discovery of PageObjects or UIObjects fails."""
