import numpy

def floatcmp(a, b):
    if (abs(a-b) < 1e-6):
        return True
    return False

def rk2(Z, Y, C, x0, x, h=0.1):
    
    while (x0 < x and floatcmp(x0, x) == False):
        k1 = Z(x0)*Y+C(x0)
        k2 = Z(x0+h)*(Y + h*k1)+C(x0+h)
        
        Y = Y + 0.5*h*(k1 + k2)
        x0 = x0+h

    return Y

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
    x1, _  = IC[1]
    
    Y = numpy.matrix([[xV],
                      [guess]])
    
    # yF is the value found by the first shot
    yF = rk2(Z, Y, C, x0, x1, 0.1)
    
    return yF

if __name__ == '__main__':
    # u'' - (1-x/5)u = x
    # u(1) = 2, u(3) = -1
    
    # u'' = (1-x/5)u + x
    
    # let v = u'
    # z = (u', u'')
    # z = (v, (1-x/5)u + x)
    
    # Move '+ x' to a constant, take coefficients
    
    # Z = (0   1, (1-x/5)u   0)
    # C = (0, x)
    # U = (u, v)
    
    
    # F = dU/dt
    #   = Z*U + C
    # Get an initial value of U
    # U = (2, -1.5)         (guess -1.5)
    
    Z = lambda x: numpy.matrix([[0, 1],[1-x/5.0, 0]])
    C = lambda x: numpy.matrix([[0], [x]])
    IC = [(1, 2), (3, -1)]
    
    guess = -1.5    
    print "My Solution: Guess: {} \tValue: {}".format(guess, shoot(Z, C, IC, guess, 2)[0,0])
    
    guess = -3.0
    print "My Solution: Guess: {} \tValue: {}".format(guess, shoot(Z, C, IC, guess, 2)[0,0])
    
    guess = -3.495
    print "My Solution: Guess: {} \tValue: {}".format(guess, shoot(Z, C, IC, guess, 2)[0,0])
    