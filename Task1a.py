import numpy
import secant
import pylab

yd = 0

def floatcmp(a, b):
    if (abs(a-b) < 1e-6):
        return True
    return False

def rk4_step(Z, Y, C, x0, h=0.1):
    k1 = Z(x0)*Y+C(x0)
    k2 = Z(x0)*(Y + 0.5*h*k1)+C(x0)
    k3 = Z(x0)*(Y + 0.5*h*k2)+C(x0)
    k4 = Z(x0)*(Y + h*k3)+C(x0)
    
    return Y + h/6.0 * (k1 + 2.0*k2 + 2.0*k3 + k4)

def rk4(Z, Y, C, x0, x, h=0.1):

    while (x0 < x and floatcmp(x0, x) == False):
        Y = rk4_step(Z, Y, C, x0, h)
        x0 = x0 + h

    return Y

def rk4_vals(Z, Y, C, x0, x, h=0.1):
    xlist = [x0]
    ylist = [Y[0,0]]

    while (x0 < x and floatcmp(x0, x) == False):
        Y = rk4_step(Z, Y, C, x0, h)
        x0 = x0 + h
        
        xlist.append(x0)
        ylist.append(Y[0,0])
        
    return (xlist, ylist)


def findyd(Z, C, IC, guessyd, guessydd):
    
    # yV is the desired value at y0, the 2nd IC
    x0, xV = IC[0]
    y0, yV = IC[1]
    
    # Use the value of xV and the guess as the starting point
    Y = numpy.matrix([[xV],
                      [guessyd],
                      [guessydd]])

    # solve the BVP for y0, return the solved value - the known value
    return rk4(Z, Y, C, x0, y0, 0.01)[0,0] - yV

def findydd(Z, C, IC, guess):
    global yd
    
    # Solve for yd at the current guess for ydd
    f = lambda x, Z=Z, C=C, IC=IC, guess=guess: findyd(Z, C, IC, x, guess)
    yd = secant.solvesecant(f, 0)

    # yV is the desired value at z0, the 3rd IC
    x0, y = IC[0]
    z0, yV = IC[2]
    
    # Use the value of xV and the guess as the starting point
    Y = numpy.matrix([[y],
                      [yd],
                      [guess]])

    # solve the BVP for z0, return the solved value - the known value
    return rk4(Z, Y, C, x0, z0, 0.01)[0,0] - yV

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
    
    IC = [(-1, -10), (0.5, 1), (1.5, -3)]
    
    f = lambda x, Z=Z, C=C, IC=IC: findydd(Z, C, IC, x)
    
    ydd = secant.solvesecant(f, 0);
    
    # Display solution
    print "Solution found at {}".format(IC[0][0])
    print "yd={} \t ydd={}".format(yd, ydd)
    
    Y = numpy.matrix([[-10],
                      [yd],
                      [ydd]])
    
    # Verify solution
    print "Check at x=  -1: {}".format(rk4(Z, Y, C, -1, -1, 0.01)[0,0])
    print "Check at x= 0.5: {}".format(rk4(Z, Y, C, -1, 0.5, 0.01)[0,0])
    print "Check at x= 1.5: {}".format(rk4(Z, Y, C, -1, 1.5, 0.01)[0,0])
    
    # Plot solution
    xlist, ylist = rk4_vals(Z, Y, C, -1, 1.5, 0.01)
    
    pylab.title("Solution to BVP")
    pylab.xlabel("x"); pylab.ylabel("y")
    Plot1, = pylab.plot(xlist, ylist, 'b-')
    pylab.grid()
    pylab.show()