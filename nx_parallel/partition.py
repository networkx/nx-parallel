import inspect
import joblib
import itertools
import networkx as nx
from functools import reduce
from typing import Optional, Iterable, Callable, Tuple, Union, List, Dict, Any
from nx_parallel.external import Backend

class NxMap:
    """Map a function to an iterable, and call distributed execution."""

    def __init__(self, func: Callable, iterator: str, backend: str = "multiprocessing", processes: Optional[int] = None):
        self.func = func
        self.backend = Backend(backend, processes)
        self.iterator = iterator

    @staticmethod
    def chunk(l: Union[List, Tuple], n: int) -> Iterable:
        """Divide a list `l` of nodes or edges into `n` chunks."""
        l_c = iter(l)
        while 1:
            x = tuple(itertools.islice(l_c, n))
            if not x:
                return
            yield x

    def create_iterables(self, G: nx.Graph, iterator: str) -> Iterable:
        """Creates an iterable of function inputs for parallel computation
        based on the provided iterator type.

        Parameters:
        -----------
        G : NetworkX graph
        iterator : str
            Type of iterator. Valid values are 'node', 'edge', 'isolate', and 'neighborhood'.
            
        Returns:
        --------
        iterable : Iterable
            An iterable of function inputs.
        """
        divisor = self.backend.processes * 4
        if iterator == 'node':
            chunks = list(self.chunk(G.nodes(), G.order() // divisor))
        elif iterator == 'edge':
            chunks = list(self.chunk(G.edges(), G.size() // divisor))
        elif iterator == 'isolate':
            isolates_list = list(nx.isolates(G))
            num_chunks = max(len(isolates_list) // divisor, 1)
            chunks = list(self.chunk(isolates_list, num_chunks))
            return chunks
        elif iterator == 'neighborhood':
            node_chunks = list(self.chunk(G.nodes(), G.order() // divisor))
            neighborhoods = [self.two_neighborhood_subset(G, chunk) for chunk in node_chunks]
            chunks = list(self.chunk(neighborhoods, len(G) // divisor))
        else:
            raise ValueError("Invalid iterator type.")
        
        num_chunks = len(chunks)
        
        if iterator in {'node', 'neighborhood'}:
            iterable = zip([G] * num_chunks, chunks, [list(G)] * num_chunks,
                           [True] * num_chunks, [None] * num_chunks)
        else:
            iterable = zip([G] * num_chunks, [None] * num_chunks,
                           [None] * num_chunks, [False] * num_chunks, chunks)
        return iterable


    def __call__(self, G: nx.Graph) -> List:
        """Call the class instance with a function and an iterable.
        The function will be called on each element of the iterable in parallel."""

        # Create iterable of function inputs for parallel computation
        iterable = self.create_iterables(G, self.iterator)

        if self.iterator == 'isolate':
            calls = [joblib.delayed(self.func)(i) for i in iterable]

            with joblib.parallel_backend('multiprocessing'):
                return joblib.Parallel(n_jobs=-1)(calls)

        params = list(inspect.signature(self.func).parameters.keys())
        calls = [joblib.delayed(self.func)(**dict(zip(params, i))) for i in iterable]
        with joblib.parallel_backend(self.backend.backend):
            return joblib.Parallel(n_jobs=self.backend.processes)(calls)


class NxReduce:
    """Reduce partial solutions to a single solution."""
    @staticmethod
    def _reduce_partial_dict_solutions(results: List[Dict]):
        if not results:
            return {}
        
        return reduce(
            lambda x, y: {k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y)}, results
        )
    
    @staticmethod
    def _reduce_partial_list_solutions(results: List[List]):
        if not results:
            return []
        return reduce(lambda x, y: x + y, results)
    
    @staticmethod
    def _reduce_partial_set_solutions(results: List[set]):
        if not results:
            return set()

        return reduce(lambda x, y: x | y, results)
    
    @staticmethod
    def reduce_partial_solutions(results: Any, method: str = "sum"):
        """Reduce partial solutions to a single solution.
        
        Parameters:
        -----------
        results : list
            List of partial solutions.
        method : str
            Method to use for reducing partial solutions. Valid values are 'sum', 'union', and 'concatenate'.
            
        Returns:
        --------
        solution : Any
            A single solution.
        """
        if method == "concatenate":
            return NxReduce._reduce_partial_dict_solutions(results)
        elif method == "union":
            return NxReduce._reduce_partial_set_solutions(results)
        elif method == "sum":
            return NxReduce._reduce_partial_list_solutions(results)
        else:
            raise ValueError("Invalid method.")
