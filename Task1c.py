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
    
def genXMatrix(f, BVs, h):
    
    XList = []
    
    XList += [f(x, h) for x in afRange(BVs[0][0]+h, BVs[-1][0], h)]
    
    return numpy.array(XList)
    
def genJMatrix(f, BVs, h):

    xV =afRange(BVs[0][0]+h, BVs[-1][0], h)
    size = len(xV)
    
    
    YList = [[0]*i +  f(x, h) + [0]*(size - 1 - i) for i,x in enumerate(xV)]
    
    return numpy.matrix(YList)[:, 2:-2]

def f(x, h):
    return [1,
            -2 + 2*h + 4*x*(h**2),
            -4*h + 2*(h**3)*(8*x + 3),
            2 + 2*h - 4*x*(h**2),
            -1]

if __name__ == '__main__':
    
    h = 0.001
    BV = [(-1, -10), (0.5, 1), (1.5, -3)]
    
    Xvals = []
    Yvals = []
    
    for i in range(2):
        BVs= BV[i:i+2]
        print BVs
        
        Xi = lambda x,h: 2*(h**3)*(x**2)
        
        X = genXMatrix(Xi, BVs, h)
        J = genJMatrix(f,  BVs, h)
        
        X[0] -= BVs[0][1] + (-2 + 2*h + 4*(BVs[0][0]+h)*(h**2))*BVs[0][1]
        X[1] -= BVs[0][1]
        
        X[-2] -= -BVs[-1][1]
        X[-1] -= (2 + 2*h - 4*(BVs[-1][0]-h)*(h**2))*BVs[-1][1] - BVs[-1][1]
        
        print i
        Xvals += afRange(BVs[0][0]+h, BVs[-1][0], h)
        Yvals += list(numpy.linalg.solve(J, X))
     
    pylab.title("Solution to BVP")
    pylab.xlabel("x"); pylab.ylabel("y")
    Plot1, = pylab.plot(Xvals, Yvals, 'b-')
    pylab.grid()
    pylab.show()
