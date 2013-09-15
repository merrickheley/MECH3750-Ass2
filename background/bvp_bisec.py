import numpy
import scipy.optimize

def floatcmp(a, b):
    if (abs(a-b) < 1e-6):
        return True
    return False

def runge4(Z, Y, C, x0, x, h=0.1):

    while (x0 < x and floatcmp(x0, x) == False):
        k1 = Z(x0)*Y+C(x0)
        k2 = Z(x0)*(Y + 0.5*h*k1)+C(x0)
        k3 = Z(x0)*(Y + 0.5*h*k2)+C(x0)
        k4 = Z(x0)*(Y + h*k3)+C(x0)
        
        Y = Y + h/6.0 * (k1 + 2.0*k2 + 2.0*k3 + k4)
        x0 = x0 + h

    return Y

def solvebisect(f, a, b, tol1=1e-6, tol2=1e-6):
    """
    Use bisection method to find roots between a and b of function f, with an accuracy of tol
    """

    fa = f(a)
    fb = f(b)
    c = 0.5*(a+b)
    #print a
    #print b
    #print fa
    #print fb

    if abs(fa) < tol1:   # Check if root is at extrema
        return a

    if abs(fb) < tol1:   # Check if root is at extrema
        return b

    if fa*fb >= 0.00:   # Check if root within range
        return None

    while True:  #Run while outside tolerance
        c = 0.5*(a+b)
        fa, fc = f(a), f(c)

        if abs(fc) < tol1 or abs(b-a)/2.0 < tol2:    # Quit when within tolerance
            return c

        if fa*fc < 0.0:    # Recalculate a or b
            b = c
        else:
            a = c
    return c

def con(Z, C, IC, guess):
    # yV is the desired value
    x0, xV = IC[0]
    y0, yV  = IC[1]
    
    # Use the value of xV and the guess as the starting point
    Y = numpy.matrix([[xV],
                      [guess]])
    
    # solve the BVP for y0, return (the value - the value of yV)
    # bisection method is a root finder, this should be 0
    return runge4(Z, Y, C, x0, y0, 0.01)[0,0] - yV

if __name__ == '__main__':
    # u'' - (1-x/5)u = x
    # u(1) = 2, u(3) = -1
     
    # Since we have been given two values, we can bisect and find u'(1)
    
    Z = lambda x: numpy.matrix([[0, 1],[1-x/5.0, 0]])
    C = lambda x: numpy.matrix([[0], [x]])
    IC = [(1, 2), (3, -1)]
    
    f = lambda x, Z=Z, C=C, IC=IC: con(Z, C, IC, x)
    
    #print "u'(1): {}".format(solvebisect(f, -10, 10))
    print "Scipy Solution: {}".format(scipy.optimize.bisect(f, -10, 10, maxiter=200))
    
    
