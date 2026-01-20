"""Custom exceptions for the LLM benchmark application."""


class BenchmarkError(Exception):
    """Base exception for benchmark-related errors."""
    pass


class APIError(BenchmarkError):
    """Exception raised for API-related errors."""
    pass


class ConfigurationError(BenchmarkError):
    """Exception raised for configuration-related errors."""
    pass


class NetworkError(BenchmarkError):
    """Exception raised for network-related errors."""
    pass