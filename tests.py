import generator as gen
import networkx as nx

def test_graph_gen():
    g, culturemat = graph_gen(2, 50, 0.2, 0.02)




def test_culture():
    avg = 0
    for i in range(500):
        d = gen.culture_init(0, 0, [[0.5,0.5],[1.0,1.0]])
        avg += d
