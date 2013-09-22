import math
import numpy

def f1(th1, th2):
    return -2*th1+0.048*math.sin(th1)+th2-1.309

def fN(th1, th2, th3):
    return th1-2*th2+0.048*math.sin(th2)+th3

def f9(th8, th9):
    return th8-2*th9+0.048*math.sin(th9)+0.3927

def phi(q):
    return -2+0.048*math.cos(q)

def J(th1, th2, th3, th4, th5, th6, th7, th8, th9):
    return numpy.array([[phi(th1), 1, 0, 0, 0, 0, 0, 0, 0],
                        [1, phi(th2), 1, 0, 0, 0, 0, 0, 0],
                        [0, 1, phi(th3), 1, 0, 0, 0, 0, 0],
                        [0, 0, 1, phi(th4), 1, 0, 0, 0, 0],
                        [0, 0, 0, 1, phi(th5), 1, 0, 0, 0],
                        [0, 0, 0, 0, 1, phi(th6), 1, 0, 0],
                        [0, 0, 0, 0, 0, 1, phi(th7), 1, 0],
                        [0, 0, 0, 0, 0, 0, 1, phi(th8), 1],
                        [0, 0, 0, 0, 0, 0, 0, 1, phi(th9)]])

def X(th1, th2, th3, th4, th5, th6, th7, th8, th9, f1, fN, f9, J):
    # solve a.x = b
    
    a = J(th1, th2, th3, th4, th5, th6, th7, th8, th9)
    
    b = numpy.array([-f1(th1, th2),
                     -fN(th1, th2, th3),
                     -fN(th2, th3, th4),
                     -fN(th3, th4, th5),
                     -fN(th4, th5, th6),
                     -fN(th5, th6, th7),
                     -fN(th6, th7, th8),
                     -fN(th7, th8, th9),
                     -f9(th8, th9)])
    return numpy.linalg.solve(a, b)

if __name__ == '__main__':
    P = numpy.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    
    for n in range(1, 1000):
        Q = P+X(P[0],P[1],P[2],P[3],P[4],P[5],P[6],P[7],P[8], f1, fN, f9, J)
        if numpy.linalg.norm(Q-P) < 1e-6:
            break
        else:
            P = Q
        
        print P


    