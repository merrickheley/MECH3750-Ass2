import math
import numpy
import pylab
import Newtons

def genFuncList(f, BVs, h):
    funcList = []
    
    s = int((BVs[-1][0] - BVs[0][0])/h) -1

    #print BVs[0][0]+h
    funcList.append(lambda y, BVs=BVs, h=h: f(BVs[0][1], y[0], y[1], BVs[0][0]+h, h))
    
    for i in range(1, s-1):
        #print  BVs[0][0]+(i+1)*h
        funcList.append(lambda y, BVs=BVs, h=h, i=i: f(y[i-1], y[i], y[i+1],  BVs[0][0]+(i+1)*h, h))

    #print BVs[0][0]+s*h
    funcList.append(lambda y, BVs=BVs, h=h, s=s: f(y[-2], y[-1], BVs[-1][1],  BVs[0][0]+s*h, h))
    
    return funcList, s

if __name__ == '__main__':
    #[ 1.1,         1.2,         1.3,         1.4,         1.5,        1.6,         1.7]
    #[ 0.85787217,  0.78041193,  0.72795581,  0.70596757,  0.73336866, 0.85952722,  1.26134775]
    
    h = 0.01
    BVs = [(1, 1), (1.8, 3)]
    f = lambda y1, y2, y3 , x, h: y1 - 2*y2 + (h**2)*((math.cos(y2) + 2)**2 - 9*(x**3)*(y2**2)) + y3
    
    funcList, num = genFuncList(f, BVs, h)
    
#     funcList = []
#     
#     funcList.append(lambda y: f(1 ,   y[0], y[1],  1.1, 0.1))
#     funcList.append(lambda y: f(y[0], y[1], y[2],  1.2, 0.1))
#     funcList.append(lambda y: f(y[1], y[2], y[3],  1.3, 0.1))
#     funcList.append(lambda y: f(y[2], y[3], y[4],  1.4, 0.1))
#     funcList.append(lambda y: f(y[3], y[4], y[5],  1.5, 0.1))
#     funcList.append(lambda y: f(y[4], y[5], y[6],  1.6, 0.1))
#     funcList.append(lambda y: f(y[5], y[6],    3,  1.7, 0.1))
    
    P = numpy.array([10.0]*num)
    
    Yvals = [BVs[0][1]]
    #Yvals.append(list(Newtons.iterativeSolve(funcList, P, h)[0]))
    Yvals += list(Newtons.iterativeSolve(funcList, P, h)[0])
    Yvals.append(BVs[-1][1])
    
    print Yvals
    
    Xvals = [BVs[0][0]+x*h for x in range(0, num+2)]
    
    pylab.title("Solution to BVP")
    pylab.xlabel("x"); pylab.ylabel("y")
    Plot1, = pylab.plot(Xvals, Yvals, 'b-')
    pylab.grid()
    pylab.show()
    
    