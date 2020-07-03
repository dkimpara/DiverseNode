import mainMethods as mmethods
import numpy as np
from sklearn.model_selection import ParameterGrid

def sayama_change_all(): #  same as sayama but change all of culture vec
    sayama_base(True)

def sayama_base(change_all):
    """change_vec = [[d1,r1,w1][d2,r2,w2]] (means of params d, culturechange)
         std_devs = [sd_culture1, sd_d, sd_rs, sd_rw],[cult2"""
    #create directory to store data
    experiment_name = 'sayama'
    mmethods.create_dir(experiment_name)

    values = np.linspace(0.0, 0.5, 6)
    param_grid = {'std_d': values, 'std_rs': values, 'std_rw': values}
    grid = ParameterGrid(param_grid)
    trials = 100
    change_vec = [[0.5, 0.5, 0.5], [0.5, 0.5, 0.5]]

    data = mmethods.run_on_grid(grid, trials, experiment_name, change_all, change_vec)
    mmethods.write_dataframe(data, trials, experiment_name)
