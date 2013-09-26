import numpy
import pylab

import Newtons

def genFuncList(f, BVs, h):
    funcList = []
    
    s = int((BVs[-1][0] - BVs[0][0])/h) -1

    #print BVs[0][0]+h
    funcList.append(lambda y, BVs=BVs, h=h: f(BVs[0][1], BVs[0][1], y[0], y[1], y[2], BVs[0][0]+h,   h))
    funcList.append(lambda y, BVs=BVs, h=h: f(BVs[0][1],      y[0], y[1], y[2], y[3], BVs[0][0]+2*h, h))
    
    for i in range(2, s-2):
        #print  BVs[0][0]+(i+1)*h
        funcList.append(lambda y, BVs=BVs, h=h, i=i: f(y[i-2], y[i-1], y[i], y[i+1], y[i+2],  BVs[0][0]+(i+1)*h, h))

    #print BVs[0][0]+s*h
    funcList.append(lambda y, BVs=BVs, h=h, s=s: f(y[-4], y[-3], y[-2],      y[-1], BVs[-1][1],  BVs[0][0]+(s-1)*h, h))
    funcList.append(lambda y, BVs=BVs, h=h, s=s: f(y[-3], y[-2], y[-1], BVs[-1][1], BVs[-1][1],  BVs[0][0]+s*h,     h))
    
    return funcList, s

def f(y1, y2, y3, y4, y5, x, h):
    #return y1 + (-2 + 2*h + 4*x*h**2)*y2 + (-4*h + 8*x + 3)*y3 \
    #        + (1 + 2*h - 4*x*h**2)*y4 - y5 - x**2
    return -(1/(2*(h**3)))*(y5- 2*y4 + 2*y2 - y1) \
            + (1/(h**2))*(y4 - 2*y3 + y2) \
            - (4*x)*(1/(2*h))*(y4 - y2) \
            + (8*x + 3)*y3 \
            - x**2

if __name__ == '__main__':
    
    h = 0.1
    BVs = [(-1, -10), (0.5, 1), (1.5, -3)]
    
    print f(-10, -8.566836952, -7.340934643, -6.26784425, -5.307783366, -0.8, 0.1)
    print f(-2.162489948, -1.50615673, -0.903244266, -0.361023112, 0.111049313, 0, 0.1)
    
    funcList, num = genFuncList(f, BVs, h)
     
    P = numpy.array([1.0]*num)
     
    Yvals = [BVs[0][1]]
    #Yvals.append(list(Newtons.iterativeSolve(funcList, P, h)[0]))
    Yvals += list(Newtons.iterativeSolve(funcList, P, h)[0])
    Yvals.append(BVs[-1][1])
     
    Xvals = [BVs[0][0]+x*h for x in range(0, num+2)]
         
    print Xvals
    print Yvals
     
    pylab.title("Solution to BVP")
    pylab.xlabel("x"); pylab.ylabel("y")
    Plot1, = pylab.plot(Xvals, Yvals, 'b-')
    pylab.grid()
    pylab.show()
