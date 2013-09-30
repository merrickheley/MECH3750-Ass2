import math
import numpy
import pylab
import Newtons

def genFuncList(f, BVs, h):
    """
    Generate a list of functions for newtons method to solve
    This sets up the equation so it can be evaluated at a set x value
    
    f:     Generic function that evaluates the equation given 3 y values, x, 
                and h
    BVs:   Array of tuples for the boundary conditions
    h:     Step Size
    """
    
    funcList = []
    
    s = int((BVs[-1][0] - BVs[0][0])/h) -1
    
    # The first function uses a boundary value
    funcList.append(lambda y, BVs=BVs, h=h: f(BVs[0][1], y[0], y[1], \
                                              BVs[0][0]+h, h))
    
    # Subsequent functions use only middle values
    for i in range(1, s-1):
        funcList.append(lambda y, BVs=BVs, h=h, i=i: f(y[i-1], y[i], y[i+1], \
                                                       BVs[0][0]+(i+1)*h, h))
    
    # The final function uses a boundary value
    funcList.append(lambda y, BVs=BVs, h=h, s=s: f(y[-2], y[-1], BVs[-1][1], \
                                                   BVs[0][0]+s*h, h))
    
    return funcList, s

if __name__ == '__main__':
    
    # Step size, boundary values, and function
    h = 0.01
    BVs = [(1, 1), (1.8, 3)]
    f = lambda y1, y2, y3 , x, h: y1 - 2*y2 + (h**2)*((math.cos(y2) + 2)**2 \
                                                      - 9*(x**3)*(y2**2)) + y3
    
    # Generate the list of functions for newtons method
    funcList, num = genFuncList(f, BVs, h)
    
    # Initial guess
    P = numpy.array([1.0]*num)

    # Values for plotting, include the values returned by Newtons solve
    Xvals = [BVs[0][0]+x*h for x in range(0, num+2)]
    Yvals = [BVs[0][1]]
    Yvals += list(Newtons.iterativeSolve(funcList, P, h)[0])
    Yvals.append(BVs[-1][1])
    
    print "Solution for h = {}".format(h)
    print numpy.array(Yvals)
    
    # Convert the Boundary values to points
    BVx = numpy.array(BVs)[:,0]
    BVy = numpy.array(BVs)[:,1]
    
    # Plot the values
    pylab.title("Solution to BVP")
    pylab.xlabel("x"); pylab.ylabel("y")
    Plot1, = pylab.plot(Xvals, Yvals, 'b-')
    Plot2, = pylab.plot(BVx, BVy, 'ro')
    pylab.grid()
    pylab.legend([Plot1, Plot2], ["Solution for y", "Boundary Values"], loc=2)
    #pylab.show()
    pylab.savefig('Task1d.png')
    