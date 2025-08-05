"""Utility functions for the project."""

import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_env_variable(var_name: str, default: str = None, required: bool = False) -> str:
    """Get environment variable or return default value.

    Args:
        var_name: Name of the environment variable
        default: Default value if environment variable is not set
        required: If True, raises an error if the variable is not set

    Returns:
        The value of the environment variable or default value with whitespace and comments stripped

    Raises:
        RuntimeError: If the environment variable is required but not set
    """
    value = os.getenv(var_name, default)
    if required and value is None:
        msg = f"Required environment variable {var_name} is not set"
        raise RuntimeError(msg)

    if value is not None:
        # Strip whitespace and any trailing comments
        value = value.split("#")[0].strip()

    return value
