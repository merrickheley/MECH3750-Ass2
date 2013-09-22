import numpy
import pylab
import math

def genXMatrix(f, h, x0, xmax):
    XList = [[f(xi, h)] for xi in numpy.arange(x0, xmax+h, h)]
    
    return numpy.matrix(XList[1:-1])

def genYMatrix(f, h, x0, xmax):
    
    maxNum = int(math.floor((xmax-x0)/h)) - 2
    
    eNumRange = enumerate(numpy.arange(x0+h, xmax, h))
    
    YList = [[0]*xn +  f(xi, h) + [0]*(maxNum - xn) for xn, xi in eNumRange]
    
    return numpy.matrix(YList)[:, 1:-1]
    
if __name__ == '__main__':
    # u'' - (1-x/5)u = x
    # u(1) = 2, u(3) = -1
    
    # Partition the region within boundary into point (x0, y0 to (xn, yn)
    # with the x_i spaced h apart
    
    # From u(1) and u(3)
    h = 0.5 
    IC = [(1, 2), (3, -1)]
    
    # Using central difference method (cdiff2)
    # u'' = h^-2 (u_(i+1) - 2u_i + u_(i-1))
    
    # sub in 
    # h^-2 (u_(i+1) - 2u_i + u_(i-1)) - (1-x/5)u_i = x_i
    # multiply by h^2
    # u_(i-1) - (2+(h^2)*(1-x/5))u_i + u_(i+1) = h^2 * x_i
    
    xFunc = lambda x,h: x*(h**2)
    yFunc = lambda x,h: [1, -(2+(h**2)*(1-x/5.0)), 1]
    
    xMat = genXMatrix(xFunc, h, IC[0][0], IC[-1][0])
    
    xMat[0,0] -= IC[0][1] 
    xMat[2,0] -= IC[-1][1]
    
    yMat = genYMatrix(yFunc, h, IC[0][0], IC[-1][0])
    
    print xMat
    print yMat
    
    soln = numpy.linalg.solve(yMat, xMat)
    soln = numpy.transpose(soln)
    soln = soln.tolist()[0]
    
    xList = numpy.arange(IC[0][0], IC[-1][0]+h, h)
    yList = [IC[0][1]] + soln + [IC[-1][1]]
    
    print "--------------------------------------------"
    
    h = 0.25
    
    xMat = genXMatrix(xFunc, h, IC[0][0], IC[-1][0])
    
    xMat[0,0] -= IC[0][1] 
    xMat[2,0] -= IC[-1][1]
    
    yMat = genYMatrix(yFunc, h, IC[0][0], IC[-1][0])
    
    print xMat
    print yMat
    
    soln = numpy.linalg.solve(yMat, xMat)
    soln = numpy.transpose(soln)
    soln = soln.tolist()[0]
    
    xList2 = numpy.arange(IC[0][0], IC[-1][0]+h, h)
    yList2 = [IC[0][1]] + soln + [IC[-1][1]]
    
    pylab.plot(xList, yList, 'b-')
    pylab.plot(xList2, yList2, 'r-')
    pylab.grid()
    pylab.show()