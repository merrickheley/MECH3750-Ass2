import numpy
import secant

def floatcmp(a, b):
    if (abs(a-b) < 1e-6):
        return True
    return False

def rk4(Z, Y, C, x0, x, h=0.1):

    while (x0 < x and floatcmp(x0, x) == False):
        k1 = Z(x0)*Y+C(x0)
        k2 = Z(x0)*(Y + 0.5*h*k1)+C(x0)
        k3 = Z(x0)*(Y + 0.5*h*k2)+C(x0)
        k4 = Z(x0)*(Y + h*k3)+C(x0)
        
        Y = Y + h/6.0 * (k1 + 2.0*k2 + 2.0*k3 + k4)
        x0 = x0 + h

    return Y

def shoot(Z, C, IC, guess, x, h=0.1):
    
    # yV is the desired value
    x0, xV = IC[0]
    y0, _  = IC[1]
    
    Y = numpy.matrix([[xV],
                      [guess]])
    
    # yF is the value found by the first shot
    yF = rk4(Z, Y, C, x0, y0, 0.01)
    
    return yF

def findyd(Z, C, IC, guess):
    # yV is the desired value
    x0, xV = IC[0]
    y0, yV = IC[1]
    
    # Use the value of xV and the guess as the starting point
    Y = numpy.matrix([[xV],
                      [guess]])
    
    # solve the BVP for y0, return (the value - the value of yV)
    # bisection method is a root finder, this should be 0
    return rk4(Z, Y, C, x0, y0, 0.01)[0,0] - yV

def findydd(Z, C, IC, guess):
    
    f = lambda x, Z=Z, C=C, IC=IC: findyd(Z, C, IC, x)
    yd = secant.solvesecant(f, 0)
    
    # yV is the desired value
    _, y = IC[0]
    y0, _ = IC[1]
    z0, yv = IC[2]
    
    # Use the value of xV and the guess as the starting point
    Y = numpy.matrix([[y],
                      [yd]
                      [guess]])

    # solve the BVP for z0, return (the value - the value of ydd)
    # bisection method is a root finder, this should be 0
    return rk4(Z, Y, C, y0, z0, 0.01)[0,0] - yv

if __name__ == '__main__':
    # -y''' + y'' - 4xy' + (8x+3)y = x^2
    # y(-1) = -10
    # y(0.5) = 1
    # y(1.5) = 1
    
    # y''' = y'' - 4xy' + (8x+3)y - x^2

    Z = lambda x:  numpy.matrix([[0, 0, 1],
                                 [0, 1, 0],
                                 [1, -4*x, 8*x+3]])
    
    C = lambda x:  numpy.matrix([[0],
                                 [0],
                                 [x**2]])
    
    IC = [(-1, -10), (0.5, 1), (1.5, 1)]
    
    f = lambda x, Z=Z, C=C, IC=IC: findydd(Z, C, IC, x)
    
    print Z(1)
    
    #print "Scipy Solution: {}".format(secant.solvesecant(f, 0))