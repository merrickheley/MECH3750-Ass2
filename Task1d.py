import math
import numpy
import pylab

def floatcmp(a, b):
    if (abs(a-b) < 1e-6):
        return True
    return False

def afRange(start, stop, step):
    
    val = start
    retList = []
    
    while (val < stop and floatcmp(val, stop) == False):
        retList.append(val)
        val += step
    
    return retList
    
def genXMatrix(f, y, IC, h):
    
    size = len(y)
    xV = afRange(IC[0][0]+h, IC[-1][0], h)
    
    XList =  [f(IC[0][1], y[0], y[1], xV[0])]
    XList += [f(y[i-1], y[i], y[i+1], xV[i]) for i in range(1, size-1)]
    XList += [f(y[-2], y[-1], IC[-1][1], xV[-1])]
    
    return numpy.array(XList)
    
def genJMatrix(f, devs, x, IC, h):
    
    size = len(x)
    border = (devs-1)/2
    xV =afRange(IC[0][0]+h, IC[-1][0], h)
    
    YList = [[0]*i +  f(x[i], xV[i]) + [0]*(size - 1 - i) for i in range(0, size)]

    return numpy.matrix(YList)[:, border:-border] 

def solveBVP(fM, fV, h, IC, dSize, guess):
    steps = int((IC[-1][0] - IC[0][0])/h)-1
    
    P = numpy.array([guess]*steps)
    
    for n in range(1000):
        a = genJMatrix(fM, dSize, P, IC, h)
        b = genXMatrix(fV, P, IC, h)
        
        Q = P + numpy.linalg.solve(a, b)
        
        norm = numpy.linalg.norm(Q-P)
        if norm < 1e-6:
            return P, norm, n
        else:
            P = Q

    return P, norm, n #None, n

if __name__ == '__main__':
    #[ 1.1,         1.2,         1.3,         1.4,         1.5,        1.6,         1.7]
    #[ 0.85787217,  0.78041193,  0.72795581,  0.70596757,  0.73336866, 0.85952722,  1.26134775]
    
    h = 0.1
    IC = [(1, 1), (1.8, 3)]
    
    fMat = lambda y, x, h=h: [1, - 2 + (h**2)*(((math.cos(y)+2)**2)/(y+1e-10) - 9*(x**3)*(y**2)), 1]
    fVal = lambda y1, y2, y3, x, h=h: -(y1 - 2*y2 + (h**2)*((math.cos(y2) + 2)**2 - 9*(x**3)*(y2**2)) + y3);
    
#     print fVal(0.85787217, 0.78041193, 0.72795581, 1.2, 0.1)
#     print fVal(0.78041193, 0.72795581, 0.70596757, 1.3) 
#     print fVal(0.72795581, 0.70596757, 0.73336866, 1.4)
#     print fVal(0.73336866, 0.85952722,  1.26134775, 1.6)
#     print "---------"
#     print fVal(0.36350875,  -0.06847174,-0.07660059, 1.3)
#     print fVal(-0.03255478, 0.06302292,  0.78967751, 1.6)   
    
    xList = afRange(IC[0][0], IC[-1][0]+h, h)   
    yList, norm, n = solveBVP(fMat, fVal, h, IC, 3, 2.0)
     
    print yList, norm, n
    yList = yList.tolist()
    
    yList = [IC[0][1]] + yList + [IC[-1][1]] 

    pylab.plot(xList, yList, 'b-')
    pylab.grid()
    pylab.show()
    