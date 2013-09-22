import math
import numpy
    
def genXMatrix(f, y, IC):
    
    size = len(y)
    
    XList =  [f(IC[0][1], y[0], y[1])]
    XList += [f(y[i], y[i+1], y[i+2]) for i in range(0, size-2)]
    XList += [f(y[-2], y[-1], IC[-1][1])]
    
    return numpy.array(XList)
    
def genJMatrix(f, devs, x):
    
    size = len(x)
    border = (devs-1)/2
    
    YList = [[0]*i +  f(x[i]) + [0]*(size - 1 - i) for i in range(0, size)]

    return numpy.matrix(YList)[:, border:-border] 

def solveBVP(fM, fV, h, IC, dSize):
    steps = int((IC[-1][0] - IC[0][0])/h)-1
    
    P = numpy.array([1.0]*steps)
    
    for n in range(1000):
        a = genJMatrix(fM, dSize, P)
        b = genXMatrix(fV, P, IC)
    
        Q = P+ numpy.linalg.solve(a, b)
        if numpy.linalg.norm(Q-P) < 1e-6:
            return P, n
        else:
            P = Q
        
    return None, n

if __name__ == '__main__':
    
    h = 0.1
    IC = [(0, -1.309), (1, 0.3927)]
    
    fMat = lambda x: [1, -2+0.048*math.sin(x), 1]
    fVal = lambda x1, x2, x3: -(x1-2*x2+0.048*math.sin(x2)+x3)
    
    print fVal(-1.309, -1.30866263, -1.26196497)
    
    print solveBVP(fMat, fVal, h, IC, 3)[0]


    