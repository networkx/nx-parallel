import os
import pytest
import networkx as nx
import nx_parallel as nxp


def test_get_n_jobs():
    """Test for various scenarios in `get_n_jobs`."""
    # Test with no n_jobs (default)
    with pytest.MonkeyPatch().context() as mp:
        mp.delitem(os.environ, "PYTEST_CURRENT_TEST", raising=False)
        assert nxp.get_n_jobs() == 1

        # Test with n_jobs set to positive value
        assert nxp.get_n_jobs(4) == 4

        # Test with n_jobs set to negative value
        assert nxp.get_n_jobs(-1) == os.cpu_count()

        # Test with joblib's context
        from joblib import parallel_config

        with parallel_config(n_jobs=3):
            assert nxp.get_n_jobs() == 3

        # Test with nx-parallel's context
        with nx.config.backends.parallel(active=True):
            assert nxp.get_n_jobs() == os.cpu_count()

        with nx.config.backends.parallel(active=True, n_jobs=5):
            assert nxp.get_n_jobs() == 5

    # Test with n_jobs = 0 to raise a ValueError
    try:
        nxp.get_n_jobs(0)
    except ValueError as e:
        assert str(e) == "n_jobs == 0 in Parallel has no meaning"


def test_chunks():
    """Test `chunks` for various input scenarios."""
    data = list(range(10))

    # Test chunking with exactly 2 larger chunks (balanced)
    chunks_list = list(nxp.chunks(data, 2))
    assert chunks_list == [(0, 1, 2, 3, 4), (5, 6, 7, 8, 9)]

    # Test chunking into 5 smaller chunks
    chunks_list = list(nxp.chunks(data, 5))
    assert chunks_list == [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]

    # Test chunking with a maximum chunk size
    chunks_list = list(nxp.chunks(data, 2, max_chunk_size=3))
    assert chunks_list == [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9,)]

    chunks_list = list(nxp.chunks(data, 5, max_chunk_size=3))
    assert chunks_list == [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]


def test_create_iterables():
    """Test `create_iterables` for different iterator types."""
    G = nx.fast_gnp_random_graph(50, 0.6, seed=42)

    # Test node iterator
    iterable = nxp.create_iterables(G, "node", 4)
    assert len(list(iterable)) == 4

    # Test edge iterator
    iterable = nxp.create_iterables(G, "edge", 4)
    assert len(list(iterable)) == 4

    # Test isolate iterator (G has no isolates, so this should be empty)
    iterable = nxp.create_iterables(G, "isolate", 4)
    assert len(list(iterable)) == 0
