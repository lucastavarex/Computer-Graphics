import sys

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
except:
    print ('\nERROR: PyOpenGL not installed properly.')
    sys.exit()

ang = 0

def display():
    glClear (GL_COLOR_BUFFER_BIT);

    global ang
    ang = (ang+1)%360
    glLoadIdentity()
    glScale(1,0.5,0.5)
    glRotatef(ang,0,0,1)
    #glRotatef(1,0,0,1)

    glBegin(GL_POLYGON);
    glColor3f (1.0, 1.0, 1.0);
    glVertex3f (-0.75, -0.75, 0.0);
    glColor3f(0,0,1);
    glVertex3f (0.75, -0.75, 0.0);
    glVertex3f (0.75, 0.75, 0.0);
    glColor3f (1.0, 1.0, 0.0);
    glVertex3f (-0.75, 0.75, 0.0);
    glEnd();

    glutSwapBuffers ();

def init ():
    glClearColor (0.0, 0.0, 0.0, 0.0);

def timer(n):
   glutPostRedisplay();
   glutTimerFunc(100,timer,0);

def reshape( width, height):
   if (height < width) :
      glViewport (int((width-height)/2),0,height,height)
   else:
      glViewport (0,int((height-width)/2),width,width)


def main():
    glutInit(sys.argv);
    glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize (250, 250); 
    glutInitWindowPosition (100, 100);
    glutCreateWindow ("hello");
    init ();
    glutDisplayFunc(display); 
    glutReshapeFunc(reshape)
    glutTimerFunc(10,timer,0);
    glutMainLoop();

main()
