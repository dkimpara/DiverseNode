##define object to keep track of connected components
# upgrade: disjoint union find implementation use nx implementation

import networkx as nx
from networkx.utils.union_find import UnionFind


class Components:
    def __init__(self, g):
        """

        :rtype: nxgraph
        """
        self.uf = UnionFind() #init uf datastruct

        g = nx.DiGraph.to_undirected(g)  # shallow copy is fine
        for c in nx.algorithms.components.connected_components(g):
            self.uf.union(*c)

    def merge(self, u, v):
        self.uf.union(u, v)

    def split(self, g):
        """reinit for now, optimize later"""
        self.__init__(g)

    def find_component(self, u):
        """returns connected component of u as set"""
        for c in self.uf.to_sets():
            if u in c:
                return c
