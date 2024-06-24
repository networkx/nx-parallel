from networkx.utils.configs import Config
from typing import Union
from dataclasses import asdict

__all__ = [
    "NxpConfig",
    "_configs",
]


class NxpConfig(Config):
    n_jobs: int = None
    backend: str = None
    return_as: str = "list"
    verbose: int = 0
    timeout: float = None
    pre_dispatch: str = "2 * n_jobs"
    batch_size: int = "auto"
    temp_folder: str = None
    max_nbytes: Union[int, str] = "1M"
    mmap_mode: str = "r"
    prefer: str = None
    require: str = None

    """
    todo: use something like this instead:
    for param_name, param in parallel_params.items():
        if param_name not in ["self", "args", "kwargs"]:  # Exclude non-configurable params
            param_name = param.default
    """

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
