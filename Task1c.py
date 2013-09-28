import numpy
import pylab
import sys

#numpy.set_printoptions(threshold=numpy.nan)

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

def getIndex(val, BVs, h):
    return int(abs(val - BVs[0][0])/h)
    
def genXMatrix(f, BVs, h):
    
    XList = []
    
    XList += [f(x, h) for x in afRange(BVs[0][0], BVs[-1][0]+h, h)]
    
    for BVi in BVs:
        XList[getIndex(BVi[0], BVs, h)] = BVi[1]
    
    return numpy.array(XList)
    
def genJMatrix(f, BVs, h):

    xV =afRange(BVs[0][0], BVs[-1][0]+h, h)
    size = len(xV)
    
    YList = [[0]*i +  f(x, h) + [0]*(size - 1 - i) for i,x in enumerate(xV)]
    YMat = numpy.matrix(YList)[:, 2:-2]
    
    for BVi in BVs:
        i = getIndex(BVi[0], BVs, h)
        YMat[i, :] = numpy.zeros((1, size))
        YMat[i, i] = 1     
    
    return YMat

def f(x, h):
    return [1.0/(2*(h**3)),
            -2.0/(2*h**3) + 1.0/(h**2) + 4.0*x/(2*h),
            -2.0/(h**2) + (8.0*x + 3.0),
            2.0/(2*h**3) + 1.0/(h**2) - 4.0*x/(2*h),
            -1.0/(2*(h**3))]
    
def fForward(x, h):
    return [0.0,
            1.0/(h**3) + 1.0/(h**2) + 4.0*x/(2*h),
            -3.0/(h**3) - 2.0/(h**2) + (8.0*x + 3.0),
            3.0/(h**3) + 1.0/(h**2) - 4.0*x/(2*h),
            -1.0/(h**3)]

def fBackward(x, h):
    return [1.0/(h**3),
            -3.0/(h**3) + 1.0/(h**2) + 4.0*x/(2*h),
            3.0/(h**3) - 2.0/(h**2) + (8.0*x + 3.0),
            -1.0/(h**3) + 1.0/(h**2) - 4.0*x/(2*h),
            0.0]

    
if __name__ == '__main__':
    
    h = 0.1
    BVs = [(-1, -10), (0.5, 1), (1.5, -3)]
    
    Xvals = []
          
    Xi = lambda x,h: (x**2)
    
    J = genJMatrix(f, BVs, h)
    X = genXMatrix(Xi, BVs, h)
    
    # Handle difference approximation at boundaries
    J[1,  0:5] = fForward(BVs[0][0]+h, h)
    J[-2, -5:] = fBackward(BVs[-1][0]+h, h)
        
    #numpy.savetxt(sys.stdout, J, '%5.2f')
    
    xlist = afRange(BVs[0][0], BVs[-1][0]+h, h) 
    ylist = numpy.linalg.solve(J, X)
    
    pylab.plot(xlist, ylist, 'b-')
    pylab.grid()
    pylab.show()
    
