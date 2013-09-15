import numpy

def floatcmp(a, b):
    if (abs(a-b) < 1e-6):
        return True
    return False

def runge2(Z, Y, x0, x, h=0.1):
    
    while (x0 < x and floatcmp(x0, x) == False):
        k1 = Z*Y
        k2 = Z*(Y + h*k1)
        
        Y = Y + 0.5*h*(k1 + k2)
        x0 = x0+h

    return Y

def runge4(Z, Y, x0, x, h=0.1):

    while (x0 < x and floatcmp(x0, x) == False):
        k1 = Z*Y
        k2 = Z*(Y + 0.5*h*k1)
        k3 = Z*(Y + 0.5*h*k2)
        k4 = Z*(Y + h*k3)
        
        Y = Y + h/6.0 * (k1 + 2.0*k2 + 2.0*k3 + k4)
        x0 = x0 + h

    return Y

if __name__ == '__main__':
    # eqn: x'' +  3x' + 2x = 0
    # x(0) = 1, x'(0) = 2
    
    # let y = x'
    #
    # z = (x', x'')
    #   = (x', -2x - 3x')      (from rearranging eqn)
    #   = (y, -2x - 3y)
    # Z = (0 1, -2 -3)
    # Y = (x, y)^T            # The values of the IC's at x0
    # F = dX/dt
    #   = Z*X
    #   = (0 1, -2 -3)*(x, y)^T
    
    Z = numpy.matrix([[0, 1],
                      [-2, -3]])
    
    Y = numpy.matrix([[1], 
                      [2]])
    
    print "My Solution: {}".format(runge2(Z, Y, 0, 0.4)[0,0])
    print "My Solution: {}".format(runge4(Z, Y, 0, 0.4)[0,0])
    
    