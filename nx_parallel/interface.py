import joblib
import itertools
import inspect
import networkx as nx
from functools import reduce
from typing import Iterable, Optional, Tuple, Union, List, Callable, Any
from collections.abc import Iterable
from nx_parallel.graph import ParallelGraph
from nx_parallel.misc import optional_package

SUPPORTED_BACKENDS = [
    "multiprocessing",
    "dask",
    "ray",
    "loky",
    "threading",
    "ipyparallel",
]

__all__ = [
    "Backends",
    "Dispatcher"
]

class Backends:
    """A context manager for specifying the backend to use for parallelization.

    Attributes
    ----------
    backend : str
        The backend to use. Choose from 'multiprocessing', 'dask', 'ray', 'loky',
        'threading', or 'ipyparallel'.
    processes : int
        The number of processes to use. If None, the number of processes will be set to
        the number of CPUs on the machine.

    Raises
    ------
    `ImportError`
        If joblib, or any of the optional backends are not installed.
    `ValueError`
        If an invalid backend is specified, or if the number of elements in the provided
        iterable is not equal to the number of parameters in the provided function.
    """

    def __init__(
        self,
        backend: str = "multiprocessing",
        processes: Optional[int] = None,
        **kwargs,
    ):
        self.backend = backend
        if processes is None:
            from os import cpu_count

            self.processes = cpu_count()
        else:
            self.processes = processes

        if self.backend not in SUPPORTED_BACKENDS:
            raise ValueError(
                f"Invalid backend specified. Choose from {SUPPORTED_BACKENDS}."
            )

        # Business logic restricted to this block
        if self.backend == "dask":
            dask, has_dask, _ = optional_package("dask")
            distributed, has_distributed, _ = optional_package("distributed")
            if not has_dask or not has_distributed:
                raise ImportError(
                    "dask[distributed] is not installed. Install dask using 'pip"
                    " install dask distributed'."
                )
            from joblib._dask import DaskDistributedBackend

            client = distributed.Client(**kwargs)
            joblib.register_parallel_backend(
                "dask", lambda: DaskDistributedBackend(client=client)
            )
        elif self.backend == "ray":
            ray, has_ray, _ = optional_package("ray")
            if not has_ray:
                raise ImportError(
                    "ray is not installed. Install ray using 'pip install ray'."
                )
            rb = ray.util.joblib.ray_backend.RayBackend(**kwargs)
            joblib.register_parallel_backend("ray", lambda: rb)
        elif self.backend == "ipyparallel":
            ipyparallel, has_ipyparallel, _ = optional_package("ipyparallel")
            if not has_ipyparallel:
                raise ImportError(
                    "ipyparallel is not installed. Install ipyparallel using 'pip "
                    "install ipyparallel'."
                )
            bview = ipyparallel.Client(**kwargs).load_balanced_view()
            joblib.register_parallel_backend(
                "ipyparallel",
                lambda: ipyparallel.joblib.IPythonParallelBackend(view=bview),
            )


class Dispatcher:
    """Generic dispatcher with conversion logic."""

    def __init__(self, func: Callable, backend: str = "multiprocessing", processes: Optional[int] = None):
        self.func = func
        self.backend = Backends(backend, processes)

    def _chunks(self, l: Union[List, Tuple], n: int) -> Iterable:
        """Divide a list `l` of nodes or edges into `n` chunks."""
        l_c = iter(l)
        while 1:
            x = tuple(itertools.islice(l_c, n))
            if not x:
                return
            yield x

    @staticmethod
    def reduce_partial_solutions(results):
        merged_results = reduce(
            lambda x, y: {k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y)}, results
        )
        return merged_results

    @staticmethod
    def convert_from_nx(incoming_graph, weight=None, *, name=None):
        """Converts NetworkX graph to ParallelGraph."""
        if isinstance(incoming_graph, nx.Graph):
            return ParallelGraph(incoming_graph)
        raise TypeError(f"Unsupported type of graph: {type(incoming_graph)}")

    @staticmethod
    def convert_to_nx(obj, *, name=None):
        """Converts ParallelGraph back to NetworkX graph."""
        if isinstance(obj, ParallelGraph):
            obj = obj.to_networkx()
        return obj

    @staticmethod
    def convert_kwargs_to_iterables(kwargs_dict):
        """Convert a dictionary of keyword arguments into a list of dictionaries,
        where each dictionary corresponds to a different combination of keyword arguments.
        """
        return [{k: v for k, v in zip(kwargs_dict.keys(), item)}
                for item in itertools.product(*[v if isinstance(v, Iterable) else [v] for v in kwargs_dict.values()])]

    def _create_node_iterables(self, p_G, **kwargs):
        """Create iterable of function node inputs for parallel computation.
        """
        node_divisor = self.backend.processes * 4
        node_chunks = list(self._chunks(p_G.nodes(), p_G.order() // node_divisor))
        num_chunks = len(node_chunks)

        # Define the iterable of function inputs for parallel computation
        iterable = zip(
            [p_G] * num_chunks,
            node_chunks,
            [list(p_G)] * num_chunks,
            [True] * num_chunks,
            [None] * num_chunks
        )
        return iterable

    def _create_edge_iterables(self, p_G, **kwargs):
        """Create iterable of function edge inputs for parallel computation.
        """
        edge_divisor = self.backend.processes * 4
        edge_chunks = list(self._chunks(p_G.edges(), p_G.size() // edge_divisor))
        num_chunks = len(edge_chunks)

        # Define the iterable of function inputs for parallel computation
        iterable = zip(
            [p_G] * num_chunks,
            [None] * num_chunks,
            [None] * num_chunks,
            [False] * num_chunks,
            edge_chunks
        )
        return iterable

    def __call__(self, G: nx.Graph, **kwargs) -> Any:
        """Call the class instance with a function and an iterable.
        The function will be called on each element of the iterable in parallel."""

        # converting graph to ParallelGraph
        p_G = self.convert_from_nx(G)

        # Create iterable of function inputs for parallel computation
        if kwargs.get("nodes", True):
            iterable = self._create_node_iterables(p_G, **kwargs)
        else:
            iterable = self._create_edge_iterables(p_G, **kwargs)

        params = list(inspect.signature(self.func).parameters.keys())

        calls = [joblib.delayed(self.func)(**dict(zip(params, i))) for i in iterable]

        with joblib.parallel_backend(self.backend.backend):
            return self.convert_to_nx(self.reduce_partial_solutions(joblib.Parallel(n_jobs=self.backend.processes, **kwargs)(calls)))
