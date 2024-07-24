from networkx.utils.configs import Config
from typing import Union
from dataclasses import asdict
import networkx as nx

__all__ = [
    "NxpConfig",
    "_configs",
    "get_curr_configs",
]


class NxpConfig(Config):
    backend: str = None
    n_jobs: int = None
    verbose: int = 0
    temp_folder: str = None
    max_nbytes: Union[int, str] = "1M"
    mmap_mode: str = "r"
    prefer: str = None
    require: str = None
    inner_max_num_threads: int = None
    backend_params: dict = None

    def get_config_dict(self, config=None):
        """Return the default configuration as a dictionary."""
        config_dict = asdict(self)
        if config is None:
            return config_dict
        elif isinstance(config, list):
            new_config = {k: config_dict[k] for k in config if k in config_dict}
            return new_config
        elif config in config_dict:
            return config_dict[config]
        else:
            raise KeyError(f"Invalid config: {config}")


_configs = NxpConfig()


def get_curr_configs(config=None):
    """Returns the current configuration settings for nx_parallel."""
    config_dict = dict(nx.config.backends.parallel)
    if config is None:
        return config_dict
    elif isinstance(config, list):
        new_config = {k: config_dict[k] for k in config if k in config_dict}
        return new_config
    elif config in config_dict:
        return config_dict[config]
    else:
        raise KeyError(f"Invalid config: {config}")


# WIP

"""
from joblib._utils import _Sentinel
from joblib.parallel import _backend, BACKENDS, EXTERNAL_BACKENDS, MAYBE_AVAILABLE_BACKENDS, DEFAULT_BACKEND
import warnings
from joblib import parallel_config

global_config = nx.config.backends.parallel

default_parallel_config = {
    "backend": _Sentinel(default_value=global_config.backend),
    "n_jobs": _Sentinel(default_value=global_config.n_jobs),
    "verbose": _Sentinel(default_value=global_config.verbose),
    "temp_folder": _Sentinel(default_value=global_config.temp_folder),
    "max_nbytes": _Sentinel(default_value=global_config.max_nbytes),
    "mmap_mode": _Sentinel(default_value=global_config.mmap_mode),
    "prefer": _Sentinel(default_value=global_config.prefer),
    "require": _Sentinel(default_value=global_config.require),
}

class nx_parallel_config(parallel_config):
    def __init__(
        self,
        backend=default_parallel_config["backend"],
        *,
        n_jobs=default_parallel_config["n_jobs"],
        verbose=default_parallel_config["verbose"],
        temp_folder=default_parallel_config["temp_folder"],
        max_nbytes=default_parallel_config["max_nbytes"],
        mmap_mode=default_parallel_config["mmap_mode"],
        prefer=default_parallel_config["prefer"],
        require=default_parallel_config["require"],
        inner_max_num_threads=None,
        **backend_params
    ):
        # Save the parallel info and set the active parallel config
        self.old_parallel_config = getattr(
            _backend, "config", default_parallel_config
        )

        backend = self._check_backend(
            backend, inner_max_num_threads, **backend_params
        )

        new_config = {
            "n_jobs": n_jobs,
            "verbose": verbose,
            "temp_folder": temp_folder,
            "max_nbytes": max_nbytes,
            "mmap_mode": mmap_mode,
            "prefer": prefer,
            "require": require,
            "backend": backend
        }
        self.parallel_config = self.old_parallel_config.copy()
        self.parallel_config.update({
            k: v for k, v in new_config.items()
            if not isinstance(v, _Sentinel)
        })

        setattr(_backend, "config", self.parallel_config)

    def _check_backend(self, backend, inner_max_num_threads, **backend_params):
        if backend is default_parallel_config['backend']:
            if inner_max_num_threads is not None or len(backend_params) > 0:
                raise ValueError(
                    "inner_max_num_threads and other constructor "
                    "parameters backend_params are only supported "
                    "when backend is not None."
                )
            return backend

        if isinstance(backend, str):
            # Handle non-registered or missing backends
            if backend not in BACKENDS:
                if backend in EXTERNAL_BACKENDS:
                    register = EXTERNAL_BACKENDS[backend]
                    register()
                elif backend in MAYBE_AVAILABLE_BACKENDS:
                    warnings.warn(
                        f"joblib backend '{backend}' is not available on "
                        f"your system, falling back to {DEFAULT_BACKEND}.",
                        UserWarning,
                        stacklevel=2
                    )
                    BACKENDS[backend] = BACKENDS[DEFAULT_BACKEND]
                else:
                    raise ValueError(
                        f"Invalid backend: {backend}, expected one of "
                        f"{sorted(BACKENDS.keys())}"
                    )

            backend = BACKENDS[backend](**backend_params)

        if inner_max_num_threads is not None:
            msg = (
                f"{backend.__class__.__name__} does not accept setting the "
                "inner_max_num_threads argument."
            )
            assert backend.supports_inner_max_num_threads, msg
            backend.inner_max_num_threads = inner_max_num_threads

        # If the nesting_level of the backend is not set previously, use the
        # nesting level from the previous active_backend to set it
        if backend.nesting_level is None:
            parent_backend = self.old_parallel_config['backend']
            if parent_backend is default_parallel_config['backend']:
                nesting_level = 0
            else:
                nesting_level = parent_backend.nesting_level
            backend.nesting_level = nesting_level

        return backend
"""

"""
import joblib
from joblib.parallel import _Sentinel

# Register the custom parallel backend
joblib.parallel.register_parallel_backend('NxpJoblibBackend', lambda **kwargs: joblib.parallel.ParallelBackendSequential(**default_parallel_config))

default_parallel_config["backend"] = _Sentinel(default_value=NxpJoblibBackend),
"""
