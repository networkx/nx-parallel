import os
from dataclasses import asdict
from functools import wraps
import networkx as nx
from joblib import parallel_config
from nx_parallel.utils.should_run_policies import default_should_run


__all__ = ["_configure_if_nx_active"]


def _configure_if_nx_active(should_run=None):
    """Decorator to set the configuration for the parallel computation
    of the nx-parallel algorithms.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if (
                nx.config.backends.parallel.active
                or "PYTEST_CURRENT_TEST" in os.environ
            ):
                # Activate nx config system in nx_parallel with:
                # `nx.config.backends.parallel.active = True`
                config_dict = asdict(nx.config.backends.parallel)
                config_dict.update(config_dict.pop("backend_params"))
                config_dict.pop("active", None)
                with parallel_config(**config_dict):
                    return func(*args, **kwargs)
            return func(*args, **kwargs)

        wrapper.should_run = default_should_run
        if should_run:
            wrapper.should_run = should_run

        return wrapper

    return decorator
