# helper functions for running sayama et all experiments
import os
from itertools import repeat
from multiprocessing import Pool
from typing import List, Any

import numpy as np
import pandas as pd
from sklearn.model_selection import ParameterGrid

import generator
import mainMethods
import simulate


def run_one_sim(s_devs):
    '''simulate and collect data'''
    g, culturemat = run_sayama_sim(s_devs)

    # analyze run
    dataDict = mainMethods.analyze(g, culturemat, True)
    if dataDict:  # if the trial succeeded
        s_devs = s_devs[0]
        dataDict['std_d'] = s_devs[1]
        dataDict['std_rs'] = s_devs[2]
        dataDict['std_rw'] = s_devs[3]  # no need to store anything else cuz sayama base sim

    return g, culturemat, dataDict


def main_sayama():
    """change_vec = [[d1,r1,w1][d2,r2,w2]] (means of params d, culturechange)
         std_devs = [sd_culture1, sd_d, sd_rs, sd_rw],[cult2"""
    # create directory to store data
    subdir = 'sayama_change_all'
    mainMethods.create_dir(subdir)

    values = np.linspace(0.0, 0.5, 6)
    param_grid = {'std_d': values, 'std_rs': values, 'std_rw': values}
    grid = ParameterGrid(param_grid)
    data: List[Any] = []
    trials = 100
    for params in grid:
        dev = [0.1, params['std_d'], params['std_rs'], params['std_rw']]
        std_devs = [dev, dev]
        data_per_iter: List[tuple] = []
        with Pool(processes=os.cpu_count() - 1) as pool:
            process = pool.map_async(run_one_sim, repeat(std_devs, trials))
            data_per_iter = process.get()  # run iters, async
            #  data is a list of tuples, one tuple g,culturemat, dataDict for each run

        # non parallel code:
        # data_per_iter = list(map(run_one_sim, repeat(std_devs, trials)))

        graphs, cultures, iter_dicts = zip(*data_per_iter)  # unzip tuples
        # save graphs for each parameter setting (100 trials)
        sayamaChangeVec = [[0.5, 0.5, 0.5], [0.5, 0.5, 0.5]]
        mainMethods.store_graphs_cultures(list(graphs), list(cultures), std_devs, sayamaChangeVec,
                                          subdir, str(dev))
        data += list(iter_dicts)  # append list of data from each sim to the main data list

    #  write all data to dataframe. tests dir already made in storegraphs method
    df = pd.DataFrame(data)  # empty dicts will be stored as NaNs
    tags = list(range(trials)) * (len(data) // trials)
    df['tags'] = tags

    df.name = subdir
    df.to_pickle('./tests/df_' + df.name)

    '''to unpickle:
    df =pd.read_pickle("./dummy.pkl")
    '''


def run_sayama_sim(std_devs):
    '''simulate a single instance'''
    # generate
    change_vec = [[0.5, 0.5, 0.5], [0.5, 0.5, 0.5]]
    g = generator.graph_gen(2, 50, 0.2, 0.02)
    culturemat = generator.culture_init(g, std_devs, change_vec)

    # simulate
    g, culturemat = simulate.simulate_iterstop(g, culturemat, True)

    return g, culturemat
