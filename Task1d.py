import math
import numpy
import pylab
import Newtons  

def floatcmp(a, b):
    if (abs(a-b) < 1e-6):
        return True
    return False

if __name__ == '__main__':
    #[ 1.1,         1.2,         1.3,         1.4,         1.5,        1.6,         1.7]
    #[ 0.85787217,  0.78041193,  0.72795581,  0.70596757,  0.73336866, 0.85952722,  1.26134775]
    
    h = 0.1
    BVs = [(1, 1), (1.8, 3)]
    
    f = lambda y1, y2, y3, x, h=h: y1 - 2*y2 + (h**2)*((math.cos(y2) + 2)**2 - 9*(x**3)*(y2**2)) + y3
    
    funcList = []
    
    funcList.append(lambda y1, y2, y3, y4, y5, y6, y7: f(1 , y1, y2,  1.1, 0.1))
    funcList.append(lambda y1, y2, y3, y4, y5, y6, y7: f(y1, y2, y3,  1.2, 0.1))
    funcList.append(lambda y1, y2, y3, y4, y5, y6, y7: f(y2, y3, y4,  1.3, 0.1))
    funcList.append(lambda y1, y2, y3, y4, y5, y6, y7: f(y3, y4, y5,  1.4, 0.1))
    funcList.append(lambda y1, y2, y3, y4, y5, y6, y7: f(y4, y5, y6,  1.5, 0.1))
    funcList.append(lambda y1, y2, y3, y4, y5, y6, y7: f(y5, y6, y7,  1.6, 0.1))
    funcList.append(lambda y1, y2, y3, y4, y5, y6, y7: f(y6, y7,  3,  1.7, 0.1))
    
    P = numpy.array([10.0]*7)
    print Newtons.iterativeSolve(funcList, P, h)
    