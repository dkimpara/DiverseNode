import os
import pickle as pk

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import analysis as analysis
from mpl_toolkits.mplot3d import Axes3D

def asnp(series):
    return np.asarray(series.values, dtype = "float")

def read_pickle(subpath):
    script_dir = os.path.dirname(__file__)
    rel_path = "tests/" + subpath 
    abs_file_path = os.path.join(script_dir, rel_path)
    with (open(abs_file_path, 'rb')) as f:
        return pk.load(f)

def scatter_gen(x, y, z, lx='x', ly='y', lz='z', colors=None, filename=None, az=305, e=27, fsize=(7,7)):
    fig = plt.figure()
    fig.set_size_inches(fsize[0],fsize[1])
    ax = fig.add_subplot(111, projection='3d')
    
    ax.scatter(x, y, z, c=colors, marker='.')
 
    ax.set_xlabel(lx)
    ax.set_ylabel(ly)
    ax.set_zlabel(lz)
    ax.view_init(elev=e, azim=az)
    plt.draw()
    if filename:
        fig.savefig(filename, dpi=100)
    return fig, ax
        
def plotfig(std, cd, spl, label, filename=None, az=305, e=27,fsize=(10,10)):
    colors = 'mbcgyr'
    c = [colors[int(i*10)] for i in std]
    scatter_gen(std, cd, spl, "s.d. of " + label,
                "|LSCC|", "<SPL>", c, filename, az, e, fsize)
          
def culture_avg_wrapper(df):
    new_col = []
    for index, row in df.iterrows():
        new_col.append(culture_avg_moved(row['c1_init'],
                                        row['c2_init'],
                                        row['c_avg_init'],
                                        row['mean_centers']))
    return new_col
            
def culture_avg_moved(c1, c2, avg_init, avg_final):
    #centers c1, c2
    v = c2 - c1
    v /= np.linalg.norm(v, 2) #create unit vector
    return np.dot((avg_final[:10] - avg_init[:10]), v[:10])


def data_cleanup(df):
    #clean up tupled dataframe
    #split df into two separate?
    new_spl = []
    new_diam = []
    components = []
    for index, row in df.iterrows():
        if isinstance(row['SPL'], tuple):
            spl, comps = row['SPL']
            d, *_ = row['diam']
        else:
            comps = 1
            d, spl = row['diam'], row['SPL']
        new_spl.append(spl)
        new_diam.append(d)
        components.append(comps)

    df.drop(columns = ['SPL', 'diam'])
    df['SPL'], df['diam'], df['comps'] = new_spl, new_diam, components
    return df

    