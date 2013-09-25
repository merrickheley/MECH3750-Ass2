import numpy

import Newtons

if __name__ == '__main__':
    # http://www.wolframalpha.com/input/?i=solve+-15x%5E2-57xy-67y%5E2+%3D+-26864190700%2C+x%5E3+%2B+3*y*x%5E2+-+2*x*y%5E2+-+7y%5E3+%3D+-604894015496000
    
    f = [lambda x,y: -(x**3 + 3*(x**2)*y - 2*x*(y**2) - 7*(y**3) + 604894015496000), 
         lambda x,y: -(-15*(x**2) - 57*x*y - 67*(y**2) + 26864190700)]
    
    P = numpy.array([-84835.0+66032.3j, 15654.4-39859.6j])
    thisSoln =  Newtons.iterativeSolve(f, P, 0.01)[0]
    
    print thisSoln