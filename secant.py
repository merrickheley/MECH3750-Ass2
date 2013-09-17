import scipy.optimize
import math

def solvesecant(f, x, tol1=1e-6, tol2=1e-6, maxiter=200):

    x0 = 1.0*x
    x1 = x0 + x0*1e-4 + 1e-4

    for _ in xrange(maxiter):
        f0, f1 = f(x0), f(x1)

        xnew = x1 - 1.0*f1*(x0 - x1)/(f0 - f1)

        if abs(x1 - x0) < tol1 or abs(f1) < tol2:
            return x1

        x0 = x1
        x1 = xnew

    return None

if __name__ == '__main__':
    f = [lambda x: 5*x + 3,
         lambda x: x**3 + 3**x + 5*x**2,
         lambda x: 5*x**5,
         lambda x: 5*x**5 - x**4 + 3**x + math.sqrt(abs(x)) + x*math.sin(x**2)]

    for i in f:
        print "Scipy Solution: {}".format(scipy.optimize.newton(i, -10, maxiter=500))
        print "My Solution: {}".format(solvesecant(i, 10, 1e-12, 1e-12, maxiter=500))
        print "----"