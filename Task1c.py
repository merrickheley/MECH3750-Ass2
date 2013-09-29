import numpy
import pylab

numpy.set_printoptions(suppress=True)

def floatcmp(a, b):
    """
    Simple float comparison. Return true for 'equal' (within threshold)
    """
    
    if (abs(a-b) < 1e-6):
        return True
    return False

def afRange(start, stop, step):
    """
    Extension to numpy's arange, but handles floats reasonably well
    """
    
    val = start
    retList = []
    
    while (val < stop and floatcmp(val, stop) == False):
        retList.append(val)
        val += step
    
    return retList

def getIndex(val, BVs, h):
    """
    Get the index for a x value given the boundary values and the step size
    
    val:   Value to get data at
    BVs:   Array of tuples for the boundary conditions
    h:     Step size
    """
    return int(abs(val - BVs[0][0])/h)
    
def genXMatrix(f, BVs, h):
    """
    Generate the right hand side matrix by evaluating f at all values of x
    between the boundary values. Set the Y value of the boundary values for
    at the correct x position.
    
    f:     Function that takes x and h to evaluate the RHS of a system of eqn.
    BVs:   Array of tuples for the boundary conditions
    h:     step size
    
    return: An array of values
    """
    
    XList = []
    
    # Construct the array
    XList += [f(x, h) for x in afRange(BVs[0][0], BVs[-1][0]+h, h)]
    
    # Handle boundary values
    for BVi in BVs:
        XList[getIndex(BVi[0], BVs, h)] = BVi[1]
    
    return numpy.array(XList)
    
def genJMatrix(f, BVs, h):
    """
    Generate a sparse Jacobian matrix. For all boundary values, fill the 
    row with zeros and set a '1' in the corresponding position.
    
    f:     Function that takes x and h to evaluate the LHS of a system of eqn.
    BVs:   Array of tuples for the boundary conditions
    h:     step size
    
    return: A non-singular jacobian
    """

    xV =afRange(BVs[0][0], BVs[-1][0]+h, h)
    size = len(xV)
    
    # Construct the jacobian
    YList = [[0]*i +  f(x, h) + [0]*(size - 1 - i) for i,x in enumerate(xV)]
    YMat = numpy.matrix(YList)[:, 2:-2]
    
    # Handle boundary values
    for BVi in BVs:
        i = getIndex(BVi[0], BVs, h)
        YMat[i, :] = numpy.zeros((1, size))
        YMat[i, i] = 1     
    
    return YMat

def f(x, h):
    """
    Evaluate the f values about point x using a third order central difference
    
    x:     point to evaluate about
    h:     step size
    
    Returns a 5-value list corresponding to
        [y_(i-2), y_(i-1), y_i, y_(i+1), y_(i+2)
    """
    return [1.0/(2*(h**3)),
            -2.0/(2*h**3) + 1.0/(h**2) + 4.0*x/(2*h),
            -2.0/(h**2) + (8.0*x + 3.0),
            2.0/(2*h**3) + 1.0/(h**2) - 4.0*x/(2*h),
            -1.0/(2*(h**3))]
    
def fForward(x, h):
    """
    Evaluate the f values about point x using a two central difference methods
    for y' and y'' and a forward difference method for y'''
    
    x: point to evaluate about
    h: step size
    
    Returns a 5-value list corresponding to
        [y_(i-2), y_(i-1), y_i, y_(i+1), y_(i+2)
    """
    return [0.0,
            1.0/(h**3) + 1.0/(h**2) + 4.0*x/(2*h),
            -3.0/(h**3) - 2.0/(h**2) + (8.0*x + 3.0),
            3.0/(h**3) + 1.0/(h**2) - 4.0*x/(2*h),
            -1.0/(h**3)]

def fBackward(x, h):
    """
    Evaluate the f values about point x using a two central difference methods
    for y' and y'' and a backward difference method for y'''
    
    x: point to evaluate about
    h: step size
    
    Returns a 5-value list corresponding to
        [y_(i-2), y_(i-1), y_i, y_(i+1), y_(i+2)
    """
    return [1.0/(h**3),
            -3.0/(h**3) + 1.0/(h**2) + 4.0*x/(2*h),
            3.0/(h**3) - 2.0/(h**2) + (8.0*x + 3.0),
            -1.0/(h**3) + 1.0/(h**2) - 4.0*x/(2*h),
            0.0]

    
if __name__ == '__main__':
    
    # step size and boundary values
    h = 0.1
    BVs = [(-1, -10), (0.5, 1), (1.5, -3)]
    
    Xvals = []
          
    Xi = lambda x,h: (x**2)
    
    # Generate the matrices
    J = genJMatrix(f, BVs, h)
    X = genXMatrix(Xi, BVs, h)
    
    # Handle difference approximation at boundaries
    J[1,  0:5] = fForward(BVs[0][0]+h, h)
    J[-2, -5:] = fBackward(BVs[-1][0]+h, h)
    
    print "X matrix:"
    print X
    
    print "J matrix:"
    print J
        
    # Get the xlist, solve for the ylist
    xlist = afRange(BVs[0][0], BVs[-1][0]+h, h) 
    ylist = numpy.linalg.solve(J, X)
    
    print "Solution list"
    print ylist
    
    # Convert the Boundary values to points
    BVx = numpy.array(BVs)[:,0]
    BVy = numpy.array(BVs)[:,1]
    
    # Plot solution
    pylab.title("Solution to BVP")
    pylab.xlabel("x"); pylab.ylabel("y")
    Plot1, = pylab.plot(xlist, ylist, 'b-')
    Plot2, = pylab.plot(BVx, BVy, 'ro')
    pylab.grid()
    pylab.legend([Plot1, Plot2], ["Solution for y", "Boundary Values"], loc=2)
    #pylab.show()
    pylab.savefig('Task1c.png')
