import numpy
import pylab

def floatcmp(a, b):
    """
    Simple float comparison. Return true for 'equal' (within threshold)
    """
    if (abs(a-b) < 1e-6):
        return True
    return False

def rk4_step(Z, Y, C, x0, h=0.1):
    """
    Compute a Runge-Kutta 4 step
    Z:     function that takes an x value and returns the matrix representing 
               a system of equations at that point
    Y:     Initial conditions for system of equations at x0
    C:     function that takes an x value and returns the constants matrix
               for the system of equations
    x0:    point to evaluate system of equations at
    h:     step size
    
    return new Y, initial conditions for system of equations at x0+h
    """
    
    F = lambda x, U: Z(x)*U + C(x)
    
    k1 = F(x0, Y)
    k2 = F(x0 + 0.5*h, Y + 0.5*h*k1)
    k3 = F(x0 + 0.5*h, Y + 0.5*h*k2)
    k4 = F(x0 + h, Y + h*k3)
    
    return Y + h/6.0 * (k1 + 2.0*k2 + 2.0*k3 + k4)

def rk4(Z, Y, C, x0, x, h=0.1):
    """
    Compute a Runge-Kutta 4 solution
    Z:     function that takes an x value and returns the matrix representing 
               a system of equations at that point
    Y:     Initial conditions for system of equations at x0
    C:     function that takes an x value and returns the constants matrix
               for the system of equations
    x0:    point to evaluate system of equations at
    x:     point to evaluate system of equations to 
    h:     step size
    
    return initial conditions for system of equations at x
    """
    
    # Run while x0 <= x
    while (x0 < x and floatcmp(x0, x) == False):
        Y = rk4_step(Z, Y, C, x0, h)
        x0 = x0 + h

    return Y

def rk4_vals(Z, Y, C, x0, x, h=0.1):
    """
    Compute a Runge-Kutta 4 solution
    Z:     function that takes an x value and returns the matrix representing 
               a system of equations at that point
    Y:     Initial conditions for system of equations at x0
    C:     function that takes an x value and returns the constants matrix
               for the system of equations
    x0:    point to evaluate system of equations at
    x:     point to evaluate system of equations to 
    h:     step size
    
    return list of x values the system was evaluated at, and their 
        corresponding y value
    """    
    
    xlist = [x0]
    ylist = [Y[0,0]]

    # Run while x0 <= x
    while (x0 < x and floatcmp(x0, x) == False):
        Y = rk4_step(Z, Y, C, x0, h)
        x0 = x0 + h
        
        xlist.append(x0)
        ylist.append(Y[0,0])
        
    return (xlist, ylist)

if __name__ == '__main__':
        # -y''' + y'' - 4xy' + (8x+3)y = x^2
    # y(-1) = -10
    # y(0.5) = 1
    # y(1.5) = -3
    
    # y''' = y'' - 4xy' + (8x+3)y - x^2

    Z = lambda x:  numpy.matrix([[0, 1, 0],
                                 [0, 0, 1],
                                 [8*x+3, -4*x, 1]])
    
    C = lambda x:  numpy.matrix([[0],
                                 [0],
                                 [-(x**2)]])
    
    h = 0.01
    
    # Boundary values
    BVs = [(-1, -10), (0.5, 1), (1.5, -3)]
    BVx = numpy.array(BVs)[:,0]
    BVy = numpy.array(BVs)[:,1]
    
    # Array of guesses
    Yguess = [[[BVs[0][1]],    [1],     [1]], 
              [[BVs[0][1]],   [50],    [50]],
              [[BVs[0][1]],  [-50],   [-50]],
              [[BVs[0][1]],   [50],   [-50]],
              [[BVs[0][1]],   [25],   [-25]],
              [[BVs[0][1]],   [13],   [-38]],
              [[BVs[0][1]],   [18],   [-32]],
              [[BVs[0][1]],   [15],   [-27]]]
    
    for i in range(len(Yguess)):
        Y = numpy.matrix(Yguess[i])
        
        print "Guesses for initial values"
        print Y
        
        # solve the BVP for y0, return the solved value - the known value
        xlist, ylist = rk4_vals(Z, Y, C, BVs[0][0], BVs[-1][0], h)
        
        print "Solution at {}".format(BVs[-1][0])
        print ylist[-1]
        
        print "--------------"
        
        pylab.title("Solution to BVP with guesses {}, {}, {}".format(*Y))
        pylab.xlabel("x"); pylab.ylabel("y")
        Plot1, = pylab.plot(xlist, ylist, 'b-')
        Plot2, = pylab.plot(BVx, BVy, 'ro')
        pylab.grid()
        pylab.legend([Plot1, Plot2], ["Solution for y", "Boundary Values"], loc=2)
        #pylab.show()
        pylab.savefig('Guess{}.png'.format(i))
        pylab.clf()