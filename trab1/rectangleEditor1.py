import sys
import numpy as np
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pyrr.matrix44 import *

shapes = []

class Rect(object):
    def __init__ (self, points, m = create_identity()):
        self.points = points
        self.set_matrix(m)
    def set_point (self, i, p):
        self.points[i] = p
    def set_matrix(self,t):
        self.m = t
        self.invm = inverse(t)
    def contains(self,p):
        p = apply_to_vector(self.invm, [p[0],p[1],0,1])
        xmin = min(self.points[0][0],self.points[1][0])
        xmax = max(self.points[0][0],self.points[1][0])
        ymin = min(self.points[0][1],self.points[1][1])
        ymax = max(self.points[0][1],self.points[1][1])
        return xmin <= p[0] <= xmax and ymin <=p[1] <= ymax
    def draw (self):
        glPushMatrix()
        glMultMatrixf(self.m)
        glRectf(*self.points[0],*self.points[1])
        glPopMatrix()

picked = None
modeConstants = ["CREATE", "TRANSLATE"]
mode = modeConstants[0]

def reshape( width, height):
    glViewport(0,0,width,height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,width,height,0)
    glMatrixMode (GL_MODELVIEW)

def mouse (button, state, x, y):
    global lastx,lasty,picked
    if state!=GLUT_DOWN: return
    if mode == "CREATE":
        shapes.append(Rect([[x,y],[x,y]]))
    elif mode == "TRANSLATE":
        picked = None
        for s in shapes:
            if s.contains([x,y]): picked = s
        lastx,lasty = x,y

def mouse_drag(x, y):
    if mode == "CREATE":
        shapes[-1].set_point(1,[x,y])
    elif mode == "TRANSLATE":
        if picked:
            global lastx,lasty
            t = create_from_translation([x-lastx,y-lasty,0])
            picked.set_matrix(multiply(picked.m,t))
            lastx,lasty=x,y
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    for s in shapes:
        glColor3f(0.4,0.4,0.4)
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        s.draw()
        glColor3f(1,0,1)
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        s.draw()
    glutSwapBuffers()

def createMenu():
    def domenu(item):
        global mode
        mode = modeConstants[item]
        return 0
    glutCreateMenu(domenu)
    for i,name in enumerate(modeConstants):
        glutAddMenuEntry(name, i)
    glutAttachMenu(GLUT_RIGHT_BUTTON)

glutInit(sys.argv);
glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB);
glutInitWindowSize (800, 600);
glutCreateWindow ("rectangle editor")
glutMouseFunc(mouse)
glutMotionFunc(mouse_drag)
glutDisplayFunc(display); 
glutReshapeFunc(reshape)
createMenu()
glutMainLoop();
