from networkx.utils.configs import Config
import joblib
import inspect
import networkx as nx
from typing import Union

__all__ = ["NxpConfig", "get_configs"]


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


def get_configs(config=None):
    parallel_params = inspect.signature(joblib.Parallel).parameters
    configs = {
        k: nx.config["backends"]["parallel"][str(k)] for k, v in parallel_params.items()
    }
    if config is None:
        return configs
    elif isinstance(config, list):
        new_configs = {k: configs[k] for k in config if k in configs}
        return new_configs
    return configs[config]


nx.config.backend_priority = [
    "parallel",
]
nx.config["backends"]["parallel"] = NxpConfig()
