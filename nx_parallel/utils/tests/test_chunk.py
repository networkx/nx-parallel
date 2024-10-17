import os
from unittest.mock import patch, call
import pytest
import networkx as nx
import nx_parallel as nxp


def test_get_n_jobs():
    """Test for various scenarios in `get_n_jobs`."""
    # Test with no n_jobs (default)
    with pytest.MonkeyPatch().context() as mp:
        mp.delitem(os.environ, "PYTEST_CURRENT_TEST", raising=False)

        # Ensure that the parallel config is inactive
        nx.config.backends.parallel.active = False
        nx.config.backends.parallel.n_jobs = None

        assert nxp.get_n_jobs() == 1

        # Test with n_jobs set to positive value
        assert nxp.get_n_jobs(4) == 4

        # Test with n_jobs set to negative value
        assert nxp.get_n_jobs(-1) == os.cpu_count()

        # Mock joblib's active backend to return ('loky', 3)
        with patch("joblib.parallel.get_active_backend", return_value=("loky", 3)):
            assert nxp.get_n_jobs() == 3

        # Test with n_jobs set in NetworkX config
        nx.config.backends.parallel.active = True
        nx.config.backends.parallel.n_jobs = 5
        assert nxp.get_n_jobs() == 5

    # Test with n_jobs = 0 to raise a ValueError
    # Ensure that the parallel config is inactive to not override n_jobs
    nx.config.backends.parallel.active = False
    nx.config.backends.parallel.n_jobs = None
    with pytest.raises(ValueError, match="n_jobs == 0 in Parallel has no meaning"):
        nxp.get_n_jobs(0)


def test_chunks():
    """Test `chunks` for various input scenarios."""
    data = list(range(10))

    # Test chunking with exactly 2 larger chunks (balanced)
    chunks_list = list(nxp.chunks(data, 2))
    assert chunks_list == [(0, 1, 2, 3, 4), (5, 6, 7, 8, 9)]

    # Test chunking into 5 smaller chunks
    chunks_list = list(nxp.chunks(data, 5))
    assert chunks_list == [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]


def test_execute_parallel_basic():
    """Basic test for `execute_parallel` to ensure it processes chunks correctly."""

    G = nx.path_graph(10)
    H = nxp.ParallelGraph(G)

    # Define a simple process_func that calculates the degree of each node in the chunk
    def process_func(G, chunk, **kwargs):
        return {node: G.degree(node) for node in chunk}

    # Define an iterator_func that returns all nodes
    def iterator_func(G):
        return list(G.nodes())  # Convert NodeView to list

    # Execute in parallel without overrides
    results = nxp.execute_parallel(
        G=H,
        process_func=process_func,
        iterator_func=iterator_func,
        get_chunks="chunks",
    )

    combined_results = {}
    for res in results:
        combined_results.update(res)

    assert combined_results == dict(G.degree())


def test_execute_parallel_with_overrides():
    """Test `execute_parallel` with overridden parallel configuration."""

    # Create a simple graph
    G = nx.complete_graph(5)
    H = nxp.ParallelGraph(G)

    # Define a simple process_func that returns the list of nodes in the chunk
    def process_func(G, chunk, **kwargs):
        return list(chunk)

    # Define an iterator_func that returns all nodes
    def iterator_func(G):
        return list(G.nodes())  # Convert NodeView to list

    # Mock joblib.Parallel in the correct module
    with patch("nx_parallel.utils.chunk.Parallel") as mock_parallel:
        with nxp.parallel_config(n_jobs=2, backend="loky", verbose=5):
            nxp.execute_parallel(
                G=H,
                process_func=process_func,
                iterator_func=iterator_func,
                get_chunks="chunks",
            )

    # Assert that Parallel was called with overridden parameters (excluding None values)
    mock_parallel.assert_called_with(
        backend="loky",
        n_jobs=2,
        verbose=5,
        max_nbytes="1M",
        mmap_mode="r",
    )


def test_execute_parallel_callable_chunks():
    """Test `execute_parallel` with a custom callable for get_chunks."""

    G = nx.cycle_graph(6)
    H = nxp.ParallelGraph(G)

    # Define a process_func that sums node numbers in the chunk
    def process_func(G, chunk, **kwargs):
        return sum(chunk)

    # Define an iterator_func that returns all nodes as a list
    def iterator_func(G):
        return list(G.nodes())  # Convert NodeView to list

    # Define a custom chunking function that groups nodes into chunks of size 2
    def custom_chunking(data):
        return [tuple(data[i : i + 2]) for i in range(0, len(data), 2)]

    results = nxp.execute_parallel(
        G=H,
        process_func=process_func,
        iterator_func=iterator_func,
        get_chunks=custom_chunking,
    )

    # Expected sums: (0+1), (2+3), (4+5) => 1, 5, 9
    expected_results = [1, 5, 9]

    assert results == expected_results


def test_parallel_config_override():
    """Test that `parallel_config` correctly overrides config within its context."""

    # Define a simple graph
    G = nx.complete_graph(5)
    H = nxp.ParallelGraph(G)

    # Define a simple process_func that returns the list of nodes in the chunk
    def process_func(G, chunk, **kwargs):
        return list(chunk)

    # Define an iterator_func that returns all nodes
    def iterator_func(G):
        return list(G.nodes())  # Convert NodeView to list

    # Mock joblib.Parallel to capture the parameters it's called with
    with patch("nx_parallel.utils.chunk.Parallel") as mock_parallel:
        with nxp.parallel_config(backend="threading", n_jobs=2, verbose=10):
            nxp.execute_parallel(
                G=H,
                process_func=process_func,
                iterator_func=iterator_func,
                get_chunks="chunks",
            )

    # Assert that Parallel was called with overridden parameters
    mock_parallel.assert_called_with(
        backend="threading",
        n_jobs=2,
        verbose=10,
        max_nbytes="1M",
        mmap_mode="r",
    )


def test_parallel_config_nested_overrides():
    """Test that nested `parallel_config` contexts correctly handle overrides."""

    G = nx.complete_graph(5)
    H = nxp.ParallelGraph(G)

    # Define a simple process_func
    def process_func(G, chunk, **kwargs):
        return list(chunk)

    # Define an iterator_func
    def iterator_func(G):
        return list(G.nodes())

    # Mock joblib.Parallel in the correct module
    with patch("nx_parallel.utils.chunk.Parallel") as mock_parallel:
        with nxp.parallel_config(backend="threading", n_jobs=2, verbose=10):
            with nxp.parallel_config(n_jobs=4, verbose=5):
                nxp.execute_parallel(
                    G=H,
                    process_func=process_func,
                    iterator_func=iterator_func,
                    get_chunks="chunks",
                )
            nxp.execute_parallel(
                G=H,
                process_func=process_func,
                iterator_func=iterator_func,
                get_chunks="chunks",
            )

        # Extract only the instantiation calls to Parallel
        instantiation_calls = [c for c in mock_parallel.call_args_list if c[0] or c[1]]

    # Adjust expected calls to exclude parameters with None values
    expected_calls = [
        call(
            backend="threading",
            n_jobs=4,
            verbose=5,
            max_nbytes="1M",
            mmap_mode="r",
        ),
        call(
            backend="threading",
            n_jobs=2,
            verbose=10,
            max_nbytes="1M",
            mmap_mode="r",
        ),
    ]

    assert instantiation_calls == expected_calls


def test_parallel_config_thread_safety(monkeypatch):
    """Test that `parallel_config` overrides are thread-safe."""

    import threading

    # Remove 'PYTEST_CURRENT_TEST' from os.environ
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)

    # Define a function to run in a thread
    def thread_func(backend, n_jobs, results, index):
        with nxp.parallel_config(backend=backend, n_jobs=n_jobs):
            # Simulate some operation that uses get_n_jobs
            job_count = nxp.get_n_jobs()
            # Retrieve backend from thread-local storage
            parallel_kwargs = getattr(
                nxp.utils.chunk._joblib_config, "parallel_kwargs", {}
            )
            backend_used = parallel_kwargs.get(
                "backend", nx.config.backends.parallel.backend
            )
            results[index] = (backend_used, job_count)

    results = {}

    # Start two threads with different configurations
    t1 = threading.Thread(target=thread_func, args=("loky", 5, results, 1))
    t2 = threading.Thread(target=thread_func, args=("threading", 3, results, 2))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # Ensure that each thread received its own overrides
    assert results[1] == ("loky", 5)
    assert results[2] == ("threading", 3)
