#simulate dynamics on graph

#global connected component class?
#optimize by making g,culturemat global?
import random

def simulate_iterstop(g, iter=500):
    '''input graph g with initialized culture state, edge weights,'''

    for i in range(iter):
        g, culturemat = sim_one_iter(g, culturemat)

    #write adj matrix and culture vec to file
    return g #for prototyping purposes.

def sim_one_iter(g, culturemat):
	
	#determine random sequence of individuals
	nodeList = list(g.nodes)
	random.shuffle(nodeList)
	
	for u in nodeList:
		#pick interaction randomly
		v  = pick_interaction(u) #with connected component class
		
		#carry out interaction
		prob_accept = p_accept(culturemat[u],culturemat[v])
		
		if random.random() < prob_accept:
			#accept culture
			#check if edge exists
			#add node?
		else:
			#reject culture
			#check for node to remove
	
    return g, culturemat

def pick_interaction(u):

	return v
def p_accept(culture_u, culture_v):
	prob = 1
	return prob