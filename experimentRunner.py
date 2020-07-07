import mainMethods as mmethods
import numpy as np
import functools
from sklearn.model_selection import ParameterGrid

import generator as gen

def change_norm(norm):


def sayama_change_all(): #  same as sayama but change all of culture vec
    sayama_base('sayam_change_all', True)

def sayama_base(experiment_name, change_all):
    """change_vec = [[d1,r1,w1][d2,r2,w2]] (means of params d, culturechange)
         std_devs = [sd_culture1, sd_d, sd_rs, sd_rw],[cult2"""
    values = np.linspace(0.0, 0.5, 6)
    param_grid = {'std_d': values, 'std_rs': values, 'std_rw': values}
    grid = ParameterGrid(param_grid)
    change_vec = [[0.5, 0.5, 0.5], [0.5, 0.5, 0.5]]

    #create graph generator func
    g_func = functools.partial(gen.graph_gen, 2, 50, 0.2, 0.02)

    #run experiment and write data. default trials=100
    mmethods.experiment_collect_store(g_func, grid, change_all, change_vec, experiment_name)