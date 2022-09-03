import math
from abc import abstractmethod
from typing import List

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from numpy.random import random


Y_MIN, Y_MAX = [-10, 10]
X_MIN, X_MAX = [-10, 10]


def draw(vertices: np.ndarray, gl_mode):
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, vertices)

    glDrawArrays(gl_mode, 0, 3)


class Point:
    x: float
    y: float
    z: float

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, other):
        return math.sqrt(
            math.pow(other.x - self.x, 2) +
            math.pow(other.y - self.y, 2)
        )


class Object:
    x: float
    y: float
    z: float

    color: np.ndarray

    scale: float

    velocity: np.ndarray

    def __init__(self,
                 x: float = 0,
                 y: float = 0,
                 z: float = 0,
                 scale: float = 1.0,
                 velocity=None,
                 color=None
                 ):

        if velocity is None:
            velocity = [0.0, 0.0, 0.0]

        if color is None:
            color = np.array([
                np.random.random(),
                np.random.random(),
                np.random.random(),
            ])

        self.x = x
        self.y = y
        self.z = z
        self.scale = scale
        self.velocity = np.array(velocity)
        self.color = color

    @abstractmethod
    def render(self):
        pass


class MeshObject(Object):
    def __init__(self, mesh_file: str, **kwargs):
        super().__init__(**kwargs)
        self.mesh = mesh_file


class Sphere(Object):
    slices: int
    stacks: int

    def __init__(self, slices=100, stacks=100, **kwargs):
        super().__init__(**kwargs)
        self.slices = slices
        self.stacks = stacks

    def render(self):
        glutWireSphere(0.5, self.slices, self.stacks)


class Scene:
    objects: List[Object]

    def __init__(self, objects: List[Object]):
        self.objects = objects

    def _physics_(self, _):
        self._move_objects_()
        self._object_collision_()

        glutPostRedisplay()

        glutTimerFunc(10, self._physics_, 0)

    def start(self):
        glutTimerFunc(10, self._physics_, 0)

    def _move_objects_(self):
        for object in self.objects:
            x, y, z = object.velocity

            object.x += x
            object.y += y
            object.z += z

    def _object_collision_(self):
        for object in self.objects:
            invert = False

            if object.x < X_MIN or object.y < Y_MIN:
                invert = True
            elif object.x > X_MAX or object.y > Y_MAX:
                invert = True

            a = Point(object.x, object.y, object.z)

            for other_object in self.objects:
                if other_object == object:
                    continue

                b = Point(other_object.x, other_object.y, other_object.z)
                distance = a.distance(b)

                print(f"distance {distance}")

                if distance < 1.0:
                    invert = True

            if invert:
                object.velocity *= -1

    def render(self):
        # self._physics_(0)

        for object in scene.objects:
            glPushMatrix()

            glTranslatef(object.x, object.y, object.z)
            glScalef(object.scale, object.scale, object.scale)
            glColor3f(object.color[0], object.color[1], object.color[2])

            object.render()

            glPopMatrix()


scene = Scene(objects=[
    Sphere(x=2, velocity=[0.05, 0.02, 0.0]),
    Sphere(x=-2, velocity=[0.04, 0.02, 0.0]),
    Sphere(x=4, velocity=[0.05, 0.02, 0.0]),
    Sphere(x=-4, velocity=[0.04, 0.02, 0.0]),
])


def keyboard(key, x, y):
    coordinate = None
    value = 0

    if key == b'q':
        exit()

    if key == b'w':
        coordinate = 1
        value = 0.1
    elif key == b's':
        coordinate = 1
        value = -0.1
    elif key == b'a':
        coordinate = 2
        value = -0.1
    elif key == b'd':
        coordinate = 2
        value = 0.1
    elif key == b't':
        velocity = [
            np.random.random() / 10,
            np.random.random() / 10,
            0.0
        ]
        scene.objects.append(Sphere(x=-4, velocity=velocity))

    if coordinate is not None:
        for object in scene.objects:
            object.velocity[coordinate-1] += value

    glutPostRedisplay()


def draw_scene():
    glClearColor(0.0, 0.7, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    scene.render()

    glutSwapBuffers()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Collision")
    scene.start()

    glutDisplayFunc(draw_scene)
    glutKeyboardFunc(keyboard)
    gluOrtho2D(X_MIN, X_MAX, Y_MIN, Y_MAX)

    glutMainLoop()


if __name__ == '__main__':
    main()
