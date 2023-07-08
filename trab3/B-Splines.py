#   Rio de Janeiro, June 10, 2023   @UFRJ - Computer Graphics
#   Professor: Cláudio Esperança
#   Subject: B-Splines
#   Author: Lucas Tavares Da Silva Ferreira
#   DRE: 120152739

#   GitHub : https://github.com/lucastavarex/Computer-Graphics

# Imports 
import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


# This section initializes the parameters and declarations needed 
# for the B-spline curve. It sets the width and height of the window, 
# the degree range of the B-spline curve, the step size for sampling,
# the control points (randomly generated), and other 
# variables for interaction.

width, height = 850, 650
degree_range = (0, 5)
step = 1
control_points = \
np.array([[100 + ((width - 200) / 5) * i, height / 2 +  np.random.uniform(-0.5, 0.5) * (height - 200)] \
                          for i in range(6)], dtype=np.float32)

nodes = np.arange(12)
selected_point = None
k = 0
d = 1
base_functions = {}

# *********************************************************************************

# This section defines the Cox-de Boor B-spline function recursively. 
# It computes the basis functions for the B-spline curve. 
# The function B(k, d, nodes) returns the basis function for the 
# control point k and degree d using the knot vector nodes. 

def B(k, d, nodes):
    if (k, d) in base_functions:
        return base_functions[(k, d)];

    if d == 0:
        def base(u):
            return 1 if nodes[k] <= u < nodes[k + 1] else 0;
    else:
        Bk0 = B(k, d - 1, nodes);
        Bk1 = B(k + 1, d - 1, nodes);
        def base(u):
            return ((u - nodes[k]) / (nodes[k + d] - nodes[k])) * Bk0(u) \
                  + ((nodes[k + d + 1] - u) / (nodes[k + d + 1] - nodes[k + 1])) * Bk1(u);
    
    base_functions[(k, d)] = base;

    return base;

# *********************************************************************************

# This section defines the function sample_curve(pts, step) that 
# samples the B-spline function for drawing. 
# It takes the control points pts and a step size step.
# It computes the weighted sum of the control points using the 
# basis functions and stores the sampled points in the sample list.

def sample_curve(pts, step=0.01):

    n = len(pts);
    b = [B(i, d, nodes) for i in range(n)];
    sample = []
    for u in np.arange(d, n, step):
        sum_point = np.zeros(2, dtype=np.float32);
        for k, p in enumerate(pts):
            w = b[k](u);
            sum_point += w * p;
        sample.append(sum_point);

    return sample;

# *********************************************************************************

# This section defines the function draw_curve() for drawing the B-spline curves using OpenGL.
# It sets up the drawing environment, sets the color and point size, and uses glBegin() and glEnd() 
# to draw the control points and the sampled points of the B-spline curve. 
# It also adds labels to the control points.

# The remaining functions (reshape(), keyboard(), mouse(), mouse_motion()) 
# handle window resizing, keyboard events, mouse events, and mouse motion, respectively. 
# These functions update the parameters of the B-spline curve accordingly.

def draw_curve():

    glClearColor(1.0, 1.0, 1.0, 1.0);
    glClear(GL_COLOR_BUFFER_BIT);

    glColor3f(0.0, 0.0, 0.0);
    glPointSize(8);
    glEnable(GL_POINT_SMOOTH);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    glBegin(GL_POINTS);
    for point in control_points:
        x, y = point;
        glVertex2f(x, y);
    glEnd();

    glColor4f(1.0, 0.0, 0.0, 0.2);
    glPointSize(5);

    glBegin(GL_POINTS)
    for point in sample_curve(control_points):
        x, y = point;
        glVertex2f(x, y);
    glEnd();

    glColor3f(0.0, 0.0, 0.0);

    for i, point in enumerate(control_points):
        x, y = point;
        glRasterPos2f(x + 8, y - 8);
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(str(i)));

    glFlush();

# *********************************************************************************

# The (reshape(), keyboard(), mouse() and mouse_motion()) 
# handle window resizing, keyboard events, mouse events, and mouse motion, respectively. 
# These functions update the parameters of the B-spline curve accordingly.


# The main() function initializes the OpenGL window, sets the display mode,
# window size, window title, and sets the event functions. 
# It then starts the main event loop using glutMainLoop(), which handles 
# interactions and drawing updates.

def reshape(w, h):
    global width, height;
    width, height = w, h;
    glViewport(0, 0, width, height);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, width, 0, height);
    glMatrixMode(GL_MODELVIEW);

def keyboard(key, x, y):
    global d;

    if key == b'd':
        d = max(d - step, degree_range[0]);
    elif key == b'D':
        d = min(d + step, degree_range[1]);

    glutPostRedisplay();

def mouse(button, state, x, y):
    global selected_point;
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            selected_point = None;
            y = height - y;
          
            for i, [px, py] in enumerate(control_points):
                d = np.sqrt((px - x) ** 2 + (py - y) ** 2);
                if d < 12:
                    selected_point = i;
                    break
        elif state == GLUT_UP:
            selected_point = None;

def mouse_motion(x, y):
    global selected_point;
    if selected_point is not None:
        y = height - y;
        control_points[selected_point] = np.array([x, y], dtype=np.float32);
    glutPostRedisplay();

def main():
    glutInit();
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA);
    glutInitWindowSize(width, height);
    glutCreateWindow(b"Trabalho 03 | Computer Graphics | B-Splines");
    glutDisplayFunc(draw_curve);
    glutReshapeFunc(reshape);
    glutMouseFunc(mouse);
    glutMotionFunc(mouse_motion);
    glutKeyboardFunc(keyboard);
    glutMainLoop();

if __name__ == "__main__":
    main()