from importlib.metadata import entry_points, EntryPoint


def test_backends_ep():
    assert entry_points(group="networkx.backends")["parallel"] == EntryPoint(
        name="parallel",
        value="nx_parallel.interface:BackendInterface",
        group="networkx.backends",
    )


def test_backend_info_ep():
    assert entry_points(group="networkx.backend_info")["parallel"] == EntryPoint(
        name="parallel", value="_nx_parallel:get_info", group="networkx.backend_info"
    )


def test_config_init():
    import networkx as nx

    assert dict(nx.config.backends.parallel) == {
        "active": True,
        "backend": "loky",
        "n_jobs": -1,
        "verbose": 0,
        "temp_folder": None,
        "max_nbytes": "1M",
        "mmap_mode": "r",
        "prefer": None,
        "require": None,
        "inner_max_num_threads": None,
        "backend_params": {},
    }
    from _nx_parallel.config import _config

    assert nx.config.backends.parallel == _config
