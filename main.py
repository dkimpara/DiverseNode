# helper functions for running sayama et all experiments

import generator
import simulate
import networkx as nx
import pickle as pk
import numpy as np
from sklearn.model_selection import ParameterGrid


# TODO: create i/o pipeline for experiments have nx.graph and culturemat
# use graph tool compatible formats “graphml”, or “gml” or pickle? try
# first
# need to figure out params to extract via nx to save on r/w time
# todo: use multiprocess


def main_sayama():  #for running sayama experiments
	"""change_vec = [[d1,r1,w1][d2,r2,w2]] (means of params d, culturechange)
	    std_devs = [sd_culture1, sd_tolerance1, sd_culture_change1, sd_w1],[cult2"""

	values = np.linspace(0.0, 0.5, 6)
	param_grid = {'std_d': values, 'std_rs': values, 'std_rw': values}
	grid = ParameterGrid(param_grid)
	for params in grid:
		graphs = []
		cultures = []
		dev = [0.1, params['std_d'], params['std_rs'], params['std_rw']]
		std_devs = [dev, dev]

		for i in range(100):  #100 iters per param setting

			g, culturemat = run_sayama_sim(std_devs)

			# analyze+extract each run
			analyze(g, culturemat) #todo use dataframe for this

			graphs.append(g)
			cultures.append(culturemat)

		# save each parameter iteration
		store_graphs_cultures(graphs,cultures, str(dev) + sayama)



def run_sayama_sim(std_devs):
	change_vec = [[0.5, 0.5, 0.5], [0.5, 0.5, 0.5]]
	#need to integrate edge change rate

	g = generator.graph_gen(2, 50, 0.2, 0.02)
	culturemat = generator.culture_init(g, std_devs, change_vec)
	g, culturemat = simulate.simulate_iterstop(g, culturemat)

	return g, culturemat


def analyze(g, culturemat):  # for analysis of sayama sim
    pass

def store_graphs_cultures(graphs, cultures, filename):  # pickle a bunch of graphs and cultures
    pass



'''sklearn example:
