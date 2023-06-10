from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *

def makeCirclePoints(n = 5, r=0.8):
    delta = pi*2/n
    for i in range(n):
        yield [r*cos(i*delta),r*sin(i*delta)]

points = [*makeCirclePoints(10)]
primitiveNames = ["GL_POINTS", "GL_LINES", "GL_LINE_STRIP", "GL_LINE_LOOP", "GL_TRIANGLES", "GL_TRIANGLE_STRIP", "GL_TRIANGLE_FAN", "GL_QUADS", "GL_QUAD_STRIP", "GL_POLYGON"]
primitiveConstants = [GL_POINTS, GL_LINES, GL_LINE_STRIP, GL_LINE_LOOP, GL_TRIANGLES, GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN, GL_QUADS, GL_QUAD_STRIP, GL_POLYGON]

primitive = GL_POINTS

def drawPrimitive(prim = GL_POINTS):
    glBegin(prim)
    for x,y in points: glVertex2f (x,y)
    glEnd()

def drawLabels():
    glColor3f(1,1,0)
    for (i,(x,y)) in enumerate(points):
        glRasterPos2f(x,y);
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord('0')+i)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1,1,1)
    glPointSize(4)
    #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    drawPrimitive(primitive)
    drawLabels()
    glutSwapBuffers()


def createMenu():
    def domenu(item):
        global primitive
        primitive = primitiveConstants[item]
        glutPostRedisplay()
        return 0
    glutCreateMenu(domenu)
    for i,name in enumerate(primitiveNames):
        glutAddMenuEntry(name, i)
    glutAttachMenu(GLUT_RIGHT_BUTTON)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
glutCreateWindow("primitives")
glutDisplayFunc(display)
createMenu()
glutMainLoop()
