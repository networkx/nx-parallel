import os
from dataclasses import asdict
from functools import wraps
import networkx as nx
from joblib import parallel_config
from joblib.parallel import get_active_backend
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
                # Peeking at joblib's current state to see if there's an outer context
                _, current_n_jobs = get_active_backend()

                # Get NetworkX config
                config_dict = asdict(nx.config.backends.parallel)
                config_dict.update(config_dict.pop("backend_params"))
                config_dict.pop("active", None)

                # SYNC: If user has an outer Joblib context for n_jobs, respect it!
                if current_n_jobs is not None:
                    config_dict["n_jobs"] = current_n_jobs

                with parallel_config(**config_dict):
                    return func(*args, **kwargs)
            return func(*args, **kwargs)

        wrapper.should_run = default_should_run
        if should_run:
            wrapper.should_run = should_run

        return wrapper

    return decorator
