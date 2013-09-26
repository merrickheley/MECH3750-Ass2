import numpy

def genJacobian(f, values, h):
    """
    Generate the jacobi matrix
    
    f: list of functions
    v: numpy array of values
    h: step size
    
    """
    
    dim = len(f)
    
    cols = []
    for i in range(0, dim):
        rows = []
        for j in range(0, dim):
            v = numpy.copy(values)
            v[j] += h
            rows.append((f[i](v) - f[i](values))/h )
            
        cols.append(rows);
        
    return numpy.asmatrix(cols)

def genX(f, values):
    return numpy.array([-fi(values) for fi in f])

def iterativeSolve(f, P, h):
    
    for n in range(1000):
        J = genJacobian(f, P, h)
        X = genX(f, P)
        
        Q = P + numpy.linalg.solve(J, X)
        
        norm = numpy.linalg.norm(Q-P)
        if norm < 1e-6:
            return P, norm, n
        else:
            P = Q

    return None, norm, n #None, n