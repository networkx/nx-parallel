from dataclasses import asdict
from joblib import parallel_config
import networkx as nx
from functools import wraps
import os

__all__ = [
    "_configure_if_nx_active",
]


def _configure_if_nx_active():
    """Decorator to set the configuration for the parallel computation
    of the nx-parallel algorithms."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if (
                nx.config.backends.parallel.active
                or "PYTEST_CURRENT_TEST" in os.environ
            ):
                # to activate nx config system in nx_parallel use:
                # `nx.config.backends.parallel.active = True`
                config_dict = asdict(nx.config.backends.parallel)
                del config_dict["active"]
                config_dict.update(config_dict["backend_params"])
                del config_dict["backend_params"]
                with parallel_config(**config_dict):
                    return func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator
