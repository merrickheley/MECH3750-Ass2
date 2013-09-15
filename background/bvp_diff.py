def cdiff1(f, h, xi):
    return (1.0/(2.0*h)) * (f(xi + h) - f(xi - h))

def cdiff2(f, h, xi):
    return (1.0/(h*h)) * (f(xi + h) - 2*f(xi) + f(xi - h))

def inc_range(a, b, stepsize=1):
    r = []
    
    while (a <= b):
        r.append(a)
        a += stepsize
        
    return r

def gen_matrix(IC, h):
    
    minIC = IC[0][0]
    maxIC = IC[-1][0]
    
    xn = inc_range(minIC, maxIC, h)
    
    u = [None]*xn.__len__()
    u[0] = IC[0][1]
    u[-1] = IC[-1][1]
    
    print u
    
    
if __name__ == '__main__':
    # u'' - (1-x/5)u = x
    # u(1) = 2, u(3) = -1
    
    # Partition the region within boundary into point (x0, y0 to (xn, yn)
    # with the x_i spaced h apart
    
    # From u(1) and u(3)
    h = 0.5    
    IC = [(1, 2), (3, -1)]

    gen_matrix(IC, h)
    
    # Using central difference method (cdiff2)
    # u'' = h^-2 (u_(i+1) - 2u_i + u_(i-1))
    
    # sub in 
    # h^-2 (u_(i+1) - 2u_i + u_(i-1)) - (1-x/5)u_i = x_i
    # multiply by h^2
    # u_(i-1) - (2+(h^2)*(1-x/5))u_i + u_(i+1) = h^2 * x_i
    
    