import planmaker
import scipy.optimize as opt
from core import fmaker
import numpy as np
import scipy.linalg as lng

def phi (x):
    global plan
    global f
    global Mep
    fux=f.make(x)
    Mx=fux*fux.T
    return -np.trace(np.dot(lng.inv(Mep),Mx))

def Meps():
    global plan
    global f
    global m
    M=np.zeros((m,m))
    for i in range(len(plan[0])):
        fu=f.make(plan[0][i])
        M+=plan[1][i]*fu*fu.T
    return M

file = open("plan.txt", "r")
plan = [[],[]]

for line in file:
    linespl = line.split()
    plan[0].append(float(linespl[0]))
    plan[1].append(float(linespl[1]))
    
f = fmaker()
f.change_model(0,"lin")
f.change_model(1,"lin")
f.change_model(2,"lin")
m = f.get_m()    
Mep = Meps()

res = opt.differential_evolution(phi,bounds=[(-1,1)])
point = res.x
val = -res.fun

print(val)