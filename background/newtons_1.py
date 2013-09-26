import numpy
import math


def genJacobian(f, values, h):
    """
    Generate the jacobi matrix
    
    f: list of functions
    v: tuple of values
    h: step size
    
    """
    
    dim = len(f)
    
    cols = []
    for i in range(0, dim):
        rows = []
        for j in range(0, dim):
            v = list(values)
            v[j] += h
            rows.append((f[i](*v) - f[i](*values))/h )
            
        cols.append(rows);
        
    return numpy.asmatrix(cols)

def genX(f, values):
    return numpy.array([-fi(*values) for fi in f])

def iterativeSolve(f, P, h):
    
    for n in range(1000):
        J = genJacobian(f, P, h)
        X = genX(f, P)
        
        
        Q = P + numpy.linalg.solve(J, P)
        
        norm = numpy.linalg.norm(Q-P)
        if norm < 1e-6:
            return P, norm, n
        else:
            P = Q

    return P, norm, n #None, n
#      

if __name__ == '__main__':
    # x^2 + y^2 = 4
    # e^x - y   = 1
    
    # f1 = x^2 + y^2 - 4
    # f2 = e^x - y - 1
    
    # F = (f1, f2)
    
    # Taylor series of a multivariate function about a point
    # P0 = (x0, y0, z0  .... ) 
    # F(x, y, z .... ) = F(P0)  + J(F(P0)) . (x - x0, y - y0, z - z0, ....)
    
    
    # J(xi, yi) = (  d/dx f1(Pi)        d/dy f1(Pi) )
    #             (  d/dx f2(Pi)        d/dy f2(Pi) )
    #
    #           = (  2*x_i               2*y_i      )
    #             (  e^(x_i)             -1         )
    
    f = [lambda x,y: x**2 + y**2 - 4, lambda x,y: math.exp(x) - y - 1]
    
    P = numpy.array([1.0, 1.0])
    
    print iterativeSolve(f, P, 0.01)
