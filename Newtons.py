import numpy

def genJacobian(f, values, h):
    """
    Generate the Jacobian matrix
    
    f:      list of functions
    values: Guess for function
    h:      step size
     
    Return the Jacobian matrix
    """
    
    dim = len(f)
    
    mats = []
    # Iterate over each row
    for i in range(0, dim):
        row = []
        # Iterate over each element
        for j in range(0, dim):
            # Calculate the derivative at the element
            v = numpy.copy(values)
            v[j] += h
            row.append((f[i](v) - f[i](values))/h )
            
        mats.append(row);
        
    return numpy.asmatrix(mats)

def genX(f, values):
    """
    Generate the X matrix
    
    f:      list of functions
    values: Guess for function
    """
    
    return numpy.array([-fi(values) for fi in f])

def iterativeSolve(f, P, h):
    """
    Iteratively solve Newtons method
    
    f:     list of functions
    P:     Initial guess for functions
    h:     Step size
    
    Return the solution matrix, the norm, and the number of iterations to 
    reach the solution.
    """
    
    # Iterate to a maximum of 1000 times
    for n in range(1000):
        # Generate X and J
        J = genJacobian(f, P, h)
        X = genX(f, P)
        
        # Solve and refine the guess
        Q = P + numpy.linalg.solve(J, X)
        
        # Once the guess has reached equilibrium, return
        norm = numpy.linalg.norm(Q-P)
        if norm < 1e-6:
            return P, norm, n
        else:
            P = Q

    return None, norm, n