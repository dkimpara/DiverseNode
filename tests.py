import generator as gen
avg = 0
for i in range(500):
    d = gen.culture_init(0, 0, [[0.5,0.5],[1.0,1.0]])
    avg += d
