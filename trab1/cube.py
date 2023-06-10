import sys

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

eye = [0,0,3]
projection = 'perspective'

def init():
   glClearColor (0.0, 0.0, 0.0, 0.0)
   glShadeModel (GL_FLAT)

def display():
   glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
   glColor3f (1.0, 1.0, 1.0)
   glMatrixMode (GL_PROJECTION)
   glLoadIdentity ()
   if projection == "perspective": 
      gluPerspective (60, 1.0, 0.1, 20)
   else:
      glOrtho (-2, 2, -2, 2, 1, 10)
   glMatrixMode (GL_MODELVIEW)
   glLoadIdentity ()             # clear the matrix
   # viewing transformation
   gluLookAt (*eye, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
   glutWireCube (1.0)
   glutSwapBuffers ()

def reshape (w, h):
   glViewport (0, 0, w, h)
   
def keyboard(key, x, y):
   d = 0.2
   increments = {
      'x':[d,0,0],
      'y':[0,d,0],
      'z':[0,0,d],
      'X':[-d,0,0],
      'Y':[0,-d,0],
      'Z':[0,0,-d]
   }   
   key = chr(ord(key))
   global projection
   if key == chr(27):
      sys.exit(0)
   elif key == "o" or key == "O":
      projection = 'ortho'
   elif key == "p" or key == "P":
      projection = 'perspective'
   elif key in increments:
      i = increments[key]
      eye[0]+=i[0]
      eye[1]+=i[1]
      eye[2]+=i[2]   
   
def timer(n):
   glutPostRedisplay();
   glutTimerFunc(100,timer,0);

glutInit(sys.argv)
glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
glutInitWindowSize (500, 500)
glutInitWindowPosition (100, 100)
glutCreateWindow ('cube')
init ()
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutTimerFunc(10,timer,0);
glutMainLoop()
