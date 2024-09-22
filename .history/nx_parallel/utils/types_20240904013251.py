import networkx as nx
from typing import Union
from enum import Enum

NX_GTYPES = Union[nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph]


class GraphIteratorType(Enum):
    NODE = "node"
    EDGE = "edge"
    ISOLATE = "isolate"
