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
    return_as: str = "list"
    timeout: float = None
    pre_dispatch: str = "2 * n_jobs"
    batch_size: int = "auto"

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
