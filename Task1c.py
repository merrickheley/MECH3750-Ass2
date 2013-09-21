import numpy

def genXMatrix(f, h, x0, xmax):
    XList = [[f(xi, h)] for xi in numpy.arange(x0, xmax+h, h)]
    
    return numpy.matrix(XList)

if __name__ == '__main__':
    
    h = 0.1
    IC = [(-1, -10), (0.5, 1), (1.5, -3)]
    
    xFunc = lambda x,h: x
    print genXMatrix(xFunc, h, IC[0][0], IC[-1][0])