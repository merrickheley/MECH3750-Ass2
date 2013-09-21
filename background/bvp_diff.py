import numpy

def genXMatrix(f, h, x0, xmax):
    XList = [[f(xi, h)] for xi in numpy.arange(x0, xmax+h, h)]
    
    return numpy.matrix(XList)

def genYMatrix(f, h, x0, xmax):
    
    eNumRange = enumerate(numpy.arange(x0, xmax+h, h))
    YList = [ f(xi, h) for xn, xi in eNumRange]
    
    
if __name__ == '__main__':
    # u'' - (1-x/5)u = x
    # u(1) = 2, u(3) = -1
    
    # Partition the region within boundary into point (x0, y0 to (xn, yn)
    # with the x_i spaced h apart
    
    # From u(1) and u(3)
    h = 0.5    
    IC = [(1, 2), (3, -1)]

    xFunc = lambda x,h: x*(h**2)
    yFunc = lambda x,h: [1, 2+(h**2)*(1-x/5.0), 1]
    
    genXMatrix(xFunc, h, IC[0][0], IC[-1][0])
    genYMatrix(yFunc, h, IC[0][0], IC[-1][0])
    
    # Using central difference method (cdiff2)
    # u'' = h^-2 (u_(i+1) - 2u_i + u_(i-1))
    
    # sub in 
    # h^-2 (u_(i+1) - 2u_i + u_(i-1)) - (1-x/5)u_i = x_i
    # multiply by h^2
    # u_(i-1) - (2+(h^2)*(1-x/5))u_i + u_(i+1) = h^2 * x_i
    
    