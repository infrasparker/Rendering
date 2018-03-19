# In the routine below, you should draw your initials in perspective

from matlib import *
from drawlib import *

def persp_initials():
    gtInitialize()

    # gtOrtho(-10, 10, -10, 10, -10, 10)
    gtPerspective(60, 100, -100)
    
    gtPushMatrix()
    gtTranslate(0, 0, 1.5)
    
    gtRotateY(50)
    gtRotateX(20)
    gtRotateZ(-10)
    
    gtScale(.05, .05, 100)
    
    gtPushMatrix()
    gtTranslate(-5, 0, 0)
    
    d()
    gtPopMatrix()
    
    gtPushMatrix()
    gtTranslate(5, 0, 0)
    w()
    gtPopMatrix()
    
    gtPopMatrix()
    
def d():
    gtBeginShape()
    
    gtVertex(-3, 5, 0)
    gtVertex(-3, -5, 0)
    
    gtVertex(-3, 5, 0)
    gtVertex(-1.5, 5, 0)
    
    gtVertex(-3, -5, 0)
    gtVertex(-1.5, -5, 0)
    
    gtPushMatrix()
    gtTranslate(-1.5, 0, 0)
    gtScale(5, 5, 0)
    
    steps = 64
    xold = 0
    yold = -1
    for i in range(steps+1):
        theta = 3.1415926535 * i / float(steps)
        x = cos(theta - 3.1415926535 / 2)
        y = sin(theta - 3.1415926535 / 2)
        gtVertex (xold, yold, 0)
        gtVertex (x, y, 0)
        xold = x
        yold = y
        
    gtPopMatrix()
    
    gtEndShape()
    
def w():
    gtBeginShape()
    
    gtVertex(-5, 5, 0)
    gtVertex(-2, -5, 0)
    
    gtVertex(-2, -5, 0)
    gtVertex(0, 0, 0)
    
    gtVertex(0, 0, 0)
    gtVertex(2, -5, 0)
    
    gtVertex(2, -5, 0)
    gtVertex(5, 5, 0)
    
    gtEndShape()
    # gtEndShape()