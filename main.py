# helper functions for running sayama et all experiments

import generator
import simulate
import networkx as nx
import pickle as pk
import numpy as np


# TODO: create i/o pipeline for experiments have nx.graph and culturemat
# use graph tool compatible formats “graphml”, or “gml” or pickle? try
# first
# need to figure out params to extract via nx to save on r/w time
# todo: use multiprocess and sklearn

def main_sayama():  #for running sayama experiments
	"""change_vec = [[d1,r1][d2,r2]] (means of params d, culturechange)
	    std_devs = [sd_culture1, sd_tolerance1, sd_culture_change1],[cult2"""
	g = generator.graph_gen(2, 50, 0.2, 0.02)
	change_vec = [[0.5, 0.5], [0.5, 0.5]]
	#need to integrate edge change rate

	#vary std_devs from 0.0 to 0.5 intervals of 0.1
	std_values = np.linspace(0.0, 0.5, 6)
	for std_d in std_values:
		for std_rs in std_values:
			for std_rw in std_values:
				dev = [0.1, std_d, std_rs]
				std_devs = [dev, dev]
				run_s

				culturemat = generator.culture_init(g, std_devs, change_vec)
				g, culturemat = simulate.simulate_iterstop(g, culturemat)


def analyze(g, culturemat):  # for analysis of sayama sim
    pass

def pickle(graphs, cultures, filename):  # pickle a bunch of graphs and cultures
    pass



'''sklearn example:
from sklearn.model_selection import ParameterGrid
values = np.linspace(0.0, 0.5, 6)
param_grid = {'a': values, 'b' : values}
grid = ParameterGrid(param_grid)
for params in grid:
    print(params['a'],params['b'])'''