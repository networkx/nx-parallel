import networkx as nx
from typing import Union

NX_GTYPES = Union[nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph]

from .chunk import *
from .decorators import *
