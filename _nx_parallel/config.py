from networkx.utils.configs import Config
from typing import Union
from dataclasses import dataclass, field

__all__ = [
    "_config",
]


@dataclass
class ParallelConfig(Config):
    active: bool = True
    backend: str = "loky"
    n_jobs: int = -1
    verbose: int = 0
    temp_folder: str = None
    max_nbytes: Union[int, str] = "1M"
    mmap_mode: str = "r"
    prefer: str = None
    require: str = None
    inner_max_num_threads: int = None
    backend_params: dict = field(default_factory=dict)


_config = ParallelConfig()
