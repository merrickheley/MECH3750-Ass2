def floatcmp(a, b):
    if (abs(a-b) < 1e-6):
        return True
    return False

def euler(f, x0, y0, x, h=0.1):

    while (x0 < x and floatcmp(x0, x) == False):
        y0 = y0 + h*f(x0, y0)
        x0 = x0+h
        
    return y0

def runge4(fdash, x0, y0, x, h = 0.1):

    while (x0 < x and floatcmp(x0, x) == False):
        k1 = fdash(x0, y0)
        k2 = fdash(x0 + 0.5*h, y0 + 0.5*h*k1)
        k3 = fdash(x0 + 0.5*h, y0 + 0.5*h*k2)
        k4 = fdash(x0 + h, y0 + h*k3)
        
        y0 = y0 + h/6.0 * (k1 + 2.0*k2 + 2.0*k3 + k4)
        x0 = x0 + h

    return y0
    
if __name__ == '__main__':
    f = lambda x,y: -2*x-y
    
    print "My Solution: {}".format(euler(f, 0, -1, 0.4))
    print "My Solution: {}".format(runge4(f, 0, -1, 0.4))