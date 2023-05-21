#   Rio de Janeiro, March 21, 2023   @UFRJ - Computer Graphics
#   Author: Lucas Tavares Da Silva Ferreira
#   DRE: 120152739
#   Professor: Cláudio Esperança
#   Subject: Shapes Editor

import sys
import numpy as np
import math

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pyrr.matrix44 import *

# These are required libraries and modules used in the code.

shapes = [] 
# Here we create an empty list called shapes to store the shapes (rectangles and circles) created by the user.

# The classes Rect and Circle define the properties and behaviors of rectangles and circles, respectively. 
# Each class has methods to set points, calculate the center, set transformation matrices,...
# ...check if a point is inside the shape, and draw the shape on the screen.

class Rect(object): #Here we define the class relative to the rectangle
    def __init__ (self, points, m = create_identity()):
        self.points = points;
        self.set_matrix(m); 
    def set_point (self, i, p):
        self.points[i] = p; 
    def get_center(self):
        center = [(self.points[0][0] + self.points[1][0]) / 2, (self.points[1][1] + self.points[0][1]) / 2];
        trans_center = apply_to_vector(self.m, [center[0], center[1], 0, 1]);
        return trans_center
    def set_matrix(self,t):
        self.m = t;
        self.invm = inverse(t);
    def contains(self,p): 
        p = apply_to_vector(self.invm, [p[0], p[1], 0, 1]); 
        xmin = min(self.points[0][0], self.points[1][0]);
        xmax = max(self.points[0][0], self.points[1][0]);
        ymin = min(self.points[0][1], self.points[1][1]);
        ymax = max(self.points[0][1], self.points[1][1]);
        return xmin <= p[0] <= xmax and ymin <=p[1] <= ymax
    def draw (self):
        glPushMatrix();
        glMultMatrixf(self.m);
        glRectf(*self.points[0], *self.points[1]);
        glPopMatrix();


class Circle(object): #Here we define the class relative to the circle
    def __init__(self, center, radius, m=create_identity()):
        self.center = center;
        self.radius = radius;
        self.set_matrix(m);
    def get_center(self): 
        trans_center = apply_to_vector(self.m, [self.center[0], self.center[1], 0, 1]);
        return trans_center
    def set_radius(self, radius):
        self.radius = radius;
    def set_matrix(self, t): 
        self.m = t;
        self.invm = inverse(t);
    def contains(self, p): 
        p = apply_to_vector(self.invm, [p[0], p[1], 0, 1]);
        dx = p[0] - self.center[0];
        dy = p[1] - self.center[1];
        return ((dx**2) + (dy**2)) <= self.radius * self.radius
    def draw(self): 
        glPushMatrix();
        glMultMatrixf(self.m);
        glBegin(GL_POLYGON);
        vertices = np.linspace(0, 360, 30);
        for vertice in vertices:
            angle = ((2)*(math.pi)*(vertice))/(360) ;
            x = self.center[0] + self.radius * math.cos(angle);
            y = self.center[1] + self.radius * math.sin(angle);
            glVertex2f(x, y);
        glEnd();
        glPopMatrix();

picked = None;
modeConstants = ["[1] - CREATE RECT", "[2] - CREATE CIRCLE", "[3] - TRANSLATE", "[4] - ROTATE", "[5] - SCALE"];
mode = modeConstants[0];

# picked is a variable that will store the shape that the user has selected for manipulation. 
# modeConstants is a list that defines the different modes of the program,...
# ...while mode is initially set to the first mode, which is creating a rectangle.

def reshape( width, height):
    glViewport(0, 0, width, height);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, width, height, 0);
    glMatrixMode (GL_MODELVIEW);

# This function is used to handle the reshaping of the window.
# It adjusts the viewport and the projection matrix to match the new window size.

def mouse (button, state, x, y): 
    global lastx, lasty, firstx, firsty, picked;
    if state!=GLUT_DOWN: return
    if mode == "[1] - CREATE RECT":
        shapes.append(Rect([[x,y],[x,y]]));
    elif mode == "[2] - CREATE CIRCLE":
        shapes.append(Circle([x, y],0));
    elif mode == "[3] - TRANSLATE":
        picked = None;
        for s in shapes:
            if s.contains([x,y]): 
                picked = s;
        lastx,lasty = x,y ;
    elif mode == "[4] - ROTATE":
        picked = None;
        for s in shapes:
            if s.contains([x,y]): 
                picked = s;
        lastx, lasty = x, y ;
    elif mode == "[5] - SCALE":
        picked = None ;
        for s in shapes:
            if s.contains([x, y]):
                picked = s;
        lastx, lasty = x, y;
        firstx, firsty = x, y;

# The mouse function handles mouse input. Depending on the current mode, it performs different actions. 
# If the mode is to create a rectangle or a circle, a new shape is created and added to the shapes list. 
# If the mode is to translate, rotate, or scale, the function checks which shape contains the clicked point... 
# ...and sets it as the picked shape for manipulation.

firstx = 0;
firsty = 0; #TODO:

def mouse_drag(x, y): 
    global lastx,lasty,firstx,firsty;
    if mode == "[1] - CREATE RECT":
        shapes[-1].set_point(1,[x,y]);
    elif mode == "[2] - CREATE CIRCLE":
        dx = x - shapes[-1].center[0];
        dy = y - shapes[-1].center[1];
        radius = math.sqrt((dx**2)+(dy**2));
        shapes[-1].set_radius(radius);
    elif mode == "[3] - TRANSLATE":
        if picked:
            translation = create_from_translation([x-lastx, y-lasty, 0]);
            picked.set_matrix(multiply(picked.m,translation));
            lastx, lasty = x, y;
    elif mode == "[4] - ROTATE":
        if picked:
            center = picked.get_center();
            last_vector = [lastx-center[0], lasty-center[1]];
            current_vector = [x-center[0],y-center[1]];
            angle = math.atan2(current_vector[1], current_vector[0])-math.atan2(last_vector[1], last_vector[0]);
            translation = create_from_translation([-center[0], -center[1], 0]);
            rotation_matrix = create_from_eulers([0, -angle, 0]);
            rtranslation = create_from_translation([center[0], center[1], 0]);
            transform_matrix = translation @ rotation_matrix @ rtranslation ;
            picked.set_matrix(picked.m @ transform_matrix);
            lastx, lasty = x, y;
    elif mode == "[5] - SCALE":
        if picked:
            center = picked.get_center();
            if center[0] != firstx or center[1] != firsty:
                scale_axis = [firstx-center[0], (firsty-center[1])];
                angle_to_x = -math.atan2(scale_axis[1], scale_axis[0]);
                mouse_axis = [x - center[0], y - center[1]];
                last_mouse_axis = [lastx - center[0], lasty - center[1]];
                proj = np.dot(mouse_axis, scale_axis) / np.linalg.norm(scale_axis);
                last_proj = np.dot(last_mouse_axis, scale_axis) / np.linalg.norm(scale_axis);
                scale_factor = proj/last_proj;
                translation = create_from_translation([-center[0], -center[1], 0]);
                rotation = create_from_eulers([0, -angle_to_x, 0]);
                scale_matrix = create_from_scale([scale_factor, 1, 1]);
                rrotation = create_from_eulers([0, angle_to_x, 0]);
                rtranslation = create_from_translation([center[0], center[1], 0]);
                transform_matrix = translation @ rotation @ scale_matrix @ rrotation @ rtranslation ;
                picked.set_matrix(picked.m @ transform_matrix) ;
                lastx, lasty = x, y;
       
    glutPostRedisplay();

# This function handles mouse dragging. Depending on the current mode and the picked shape, it performs different transformations. 
# If the mode is to create a rectangle or a circle, it updates the dimensions of the shape based on the dragged distance. 
# If the mode is to translate, rotate, or scale, it calculates the necessary transformations based on the dragged distance... 
# ...and updates the picked shape accordingly.

def display():
    glClear(GL_COLOR_BUFFER_BIT);
    for s in shapes:
        if isinstance(s, Circle):
            glColor3f(0.4,0.4,0.4);
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL);
            s.draw();
            glColor3f(1,1,1);
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE);
            s.draw();
        else:
            glColor3f(0.4,0.4,0.4);
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL);
            s.draw();
            glColor3f(1,1,1);
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE);
            s.draw();
    glutSwapBuffers();

# This function is responsible for the display. It clears the screen, sets the modelview matrix,...
# ...and then iterates through the shapes list, calling the draw method for each shape to render it on the screen. 
# Finally, it swaps the buffers to update the display.

def createMenu():
    def domenu(item):
        global mode;
        mode = modeConstants[item];
        return 0
    glutCreateMenu(domenu);
    for i,name in enumerate(modeConstants):
        glutAddMenuEntry(name, i);
    glutAttachMenu(GLUT_RIGHT_BUTTON);

glutInit(sys.argv);
glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB);
glutInitWindowSize (800, 600);
glutCreateWindow ("EEL882 - Computer Graphics - Task 1 (Shapes editor)");
glutMouseFunc(mouse);
glutMotionFunc(mouse_drag);
glutDisplayFunc(display);
glutReshapeFunc(reshape);
createMenu()
glutMainLoop();

# This is the main function sets up the window and its properties, registers the callback functions for reshaping,...
# ...displaying, mouse input, mouse dragging, and enters the main event processing loop using glutMainLoop().