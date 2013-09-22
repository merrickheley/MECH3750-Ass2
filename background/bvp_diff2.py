import math
import numpy
import pylab
    
def genXMatrix(f, y, IC):
    
    size = len(y)
    xV = numpy.arange(IC[0][0]+h, IC[-1][0], h)
    
    XList =  [f(IC[0][1], y[0], y[1], xV[0])]
    XList += [f(y[i-1], y[i], y[i+1], xV[i]) for i in range(1, size-1)]
    XList += [f(y[-2], y[-1], IC[-1][1], xV[-1])]
    
    return numpy.array(XList)
    
def genJMatrix(f, devs, x):
    
    size = len(x)
    border = (devs-1)/2
    xV = numpy.arange(IC[0][0]+h, IC[-1][0], h)
    
    YList = [[0]*i +  f(x[i], xV[i]) + [0]*(size - 1 - i) for i in range(0, size)]

    return numpy.matrix(YList)[:, border:-border] 

def solveBVP(fM, fV, h, IC, dSize):
    steps = int((IC[-1][0] - IC[0][0])/h)-1
    
    P = numpy.array([0.0]*steps)
    
    for n in range(1000):
        a = genJMatrix(fM, dSize, P)
        b = genXMatrix(fV, P, IC)

        Q = P + numpy.linalg.solve(a, b)
        
        if numpy.linalg.norm(Q-P) < 1e-6:
            return P, n
        else:
            P = Q
            
    return None, n

if __name__ == '__main__':
    
    h = 0.01
    IC = [(1, 2), (3, -1)]
    
    fMat = lambda y, x, h=h: [1, -2-(h**2)*(1-x/5.0), 1]
    fVal = lambda y1, y2, y3, x, h=h: (h**2)*x-(y1-(2+(h**2)*(1-x/5.0))*y2+y3)
    
    xList = numpy.arange(IC[0][0], IC[-1][0]+h, h)
    yList = solveBVP(fMat, fVal, h, IC, 3)[0]
    yList = yList.tolist()
    
    yList = [IC[0][1]] + yList + [IC[-1][1]] 
    
    print len(xList)
    print len(yList)

    pylab.plot(xList, yList, 'b-')
    pylab.grid()
    pylab.show()
    