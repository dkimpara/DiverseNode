import os
import pickle as pk

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import analysis as analysis
from mpl_toolkits.mplot3d import Axes3D

def read_pickle(subpath):
    script_dir = os.path.dirname(__file__)
    rel_path = "tests/" + subpath 
    abs_file_path = os.path.join(script_dir, rel_path)
    with (open(abs_file_path, 'rb')) as f:
        return pk.load(f)

    
def plotfig(std, cd, spl, label):
    fig = plt.figure()
    fig.set_size_inches(10, 10)
    ax = fig.add_subplot(111, projection='3d')
    colors = 'mbcgyr'
    c = [colors[int(i*10)] for i in std]
    ax.scatter(std, cd, spl, c=c, marker='.')


    ax.set_xlabel("s.d. of " + label)
    ax.set_ylabel("<CD>")
    ax.set_zlabel("<SPL>")
    ax.view_init(elev=27, azim=305)
    plt.draw()
    fig.savefig('test2png.png', dpi=100)