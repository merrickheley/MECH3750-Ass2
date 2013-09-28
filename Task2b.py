import numpy
import Newtons

if __name__ == '__main__':
    
    # Functions to be solved, v[0] is x, v[1] is y
    f = [lambda v: -(v[0]**3 + 3*(v[0]**2)*v[1] - 2*v[0]*(v[1]**2) \
                     - 7*(v[1]**3) + 604894015496000), 
         lambda v: -(-15*(v[0]**2) - 57*v[0]*v[1] - 67*(v[1]**2) \
                     + 26864190700)]
        
    guesses = [[ 1 + 1j,  1 + 1j],
               [ 1 - 1j,  1 - 1j],
               [-100 - 100j, -100 - 100j],
               [-100 + 100j, -100 + 100j],
               [100000 + 100000j, 100000 + 100000j],
               [100000 - 100000j, 100000 - 100000j]]
        
    for i in xrange(len(guesses)):
        # Guess
        P = numpy.array(guesses[i])
     
        # Solve
        print  Newtons.iterativeSolve(f, P, 0.01)[0]