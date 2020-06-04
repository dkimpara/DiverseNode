##define object to keep track of connected components

import networkx as nx

class Components:
    def __init__(self, g):
        g = nx.DiGraph.to_undirected(g) #shallow copy is fine
        self.list_sets = list(nx.algorithms.components.connected_components(g))
		
		print(t)
     
    def merge(self, c1, c2):
				
    def split(self, g):
		g = nx.DiGraph.to_undirected(g) #shallow copy is fine
		self.list_sets = list(nx.algorithms.components.connected_components(g))
	
    def find_component(self, u):
		"""returns connected component of u as set"""
		for c in self.gen_sets:
			if u in c: return c
		
		raise ValueError('connected component not found')
			
