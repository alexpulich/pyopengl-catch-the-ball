import random

from OpenGL.GL import *
import glfw

from pyrr import matrix44, matrix33, Vector3

from primitives import Cube, Sphere, Heart
from utils import Textureloader


PROJECTION_NEAR = 0.1
PROJECTION_FAR = 100.0

DEFAULT_VIEW = [0.0, -2.5, -8.0]


class SphereGameObject(Sphere):
    """ Implements OpenGL sphere object """
    VAO = None
    VBO = None
    EBO = None

    # initial position
    pos = [2.0, 0.0, 0.0]

    # initial scale
    scale = 0.5

    shader = None
    texture = None

    def __init__(self, texture_path=None, pos=None):
        """ Creates and binds buffers, sets initial position of the object, loads and binds texture """
        super().__init__()

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.itemsize * len(self.vertices), self.vertices, GL_STATIC_DRAW)

        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.itemsize * len(self.indices), self.indices, GL_STATIC_DRAW)

        # position
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.vertices.itemsize * 5, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # textures
        if texture_path:
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.vertices.itemsize * 5, ctypes.c_void_p(12))
            glEnableVertexAttribArray(1)
            self.texture = Textureloader.load(texture_path)

        if pos:
            self.pos = pos

    def prep(self, shader, aspect_ratio, scale_val=None, angle=90.0):
        """ Sets object's shader and enables it, sets scale and computes view and projection matrices """
        self.shader = shader
        self.shader.use()

        if scale_val:
            self.scale = scale_val

        view = matrix44.create_from_translation(Vector3(DEFAULT_VIEW))
        self.shader.set_mat4('view', view)

        projection = matrix44.create_perspective_projection_matrix(angle, aspect_ratio, PROJECTION_NEAR, PROJECTION_FAR)
        self.shader.set_mat4('projection', projection)

        scale = matrix33.create_from_scale(Vector3([self.scale, self.scale, self.scale]))
        scale = matrix44.create_from_matrix33(scale)
        self.shader.set_mat4('scale', scale)

    def draw(self):
        """ Draws the object """
        self.shader.use()

        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)

        model = matrix44.create_from_translation(Vector3(self.pos))
        glBindTexture(GL_TEXTURE_2D, self.texture)
        self.shader.set_mat4('model', model)
        glDrawElements(GL_LINE_LOOP, len(self.indices), GL_UNSIGNED_INT, None)


class Ball(SphereGameObject):
    """ Implements falling ball object """
    INITIAL_SPEED = 0.02
    speed = INITIAL_SPEED

    def __init__(self, texture_path):
        super().__init__(texture_path, self.random_pos())

    def random_pos(self):
        self.pos = [random.uniform(-5, 5), 6.1, 0.0]

    def draw(self, move):
        if move:
            self.move()
        super().draw()

    def move(self):
        """ Move objects along y axis with constant speed"""
        self.pos[1] = self.pos[1] - self.speed


class LiveHeart(Heart):
    """ Implements OpenGL heart objects (show player's lifes"""
    VAO = None
    VBO = None
    EBO = None

    # initial scale
    scale = 1.0

    shader = None

    def __init__(self, pos):
        super().__init__()

        self.pos = pos

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.itemsize * len(self.vertices), self.vertices, GL_STATIC_DRAW)

        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.itemsize * len(self.indices), self.indices, GL_STATIC_DRAW)

        # position
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.vertices.itemsize * 3, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

    def prep(self, shader, aspect_ratio, scale_val=None, angle=90.0):
        self.shader = shader
        self.shader.use()

        if scale_val:
            self.scale = scale_val

        view = matrix44.create_from_translation(Vector3(DEFAULT_VIEW))
        self.shader.set_mat4('view', view)

        projection = matrix44.create_perspective_projection_matrix(angle, aspect_ratio, PROJECTION_NEAR, PROJECTION_FAR)
        self.shader.set_mat4('projection', projection)

        scale = matrix33.create_from_scale(Vector3([self.scale, self.scale, self.scale]))
        scale = matrix44.create_from_matrix33(scale)
        self.shader.set_mat4('scale', scale)

    def draw(self):
        self.shader.use()
        glBindVertexArray(self.VAO)
        glEnable(GL_PRIMITIVE_RESTART)
        glPrimitiveRestartIndex(GL_PRIMITIVE_RESTART_FIXED_INDEX)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)

        model = matrix44.create_from_translation(Vector3(self.pos))
        self.shader.set_mat4('model', model)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)


class CubeGameObject(Cube):
    VAO = None
    VBO = None
    EBO = None

    pos = [0.0, 0.0, 0.0]
    scale = 1.0

    shader = None
    texture = None

    def __init__(self, texture_path=None, pos=None):
        super().__init__()

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.itemsize * len(self.vertices), self.vertices, GL_STATIC_DRAW)

        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.itemsize * len(self.indices), self.indices, GL_STATIC_DRAW)

        # position
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.vertices.itemsize * 5, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # textures
        if (texture_path):
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.vertices.itemsize * 5, ctypes.c_void_p(12))
            glEnableVertexAttribArray(1)
            self.texture = Textureloader.load(texture_path)

        if pos:
            self.pos = pos

    def prep(self, shader, aspect_ratio, scale_val=None, angle=90.0):
        self.shader = shader
        self.shader.use()

        if scale_val:
            self.scale = scale_val

        view = matrix44.create_from_translation(Vector3(DEFAULT_VIEW))
        self.shader.set_mat4('view', view)

        projection = matrix44.create_perspective_projection_matrix(angle, aspect_ratio, PROJECTION_NEAR, PROJECTION_FAR)
        self.shader.set_mat4('projection', projection)

        scale = matrix33.create_from_scale(Vector3([self.scale, self.scale, self.scale]))
        scale = matrix44.create_from_matrix33(scale)
        self.shader.set_mat4('scale', scale)

    def draw(self):
        self.shader.use()

        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)

        model = matrix44.create_from_translation(Vector3(self.pos))
        glBindTexture(GL_TEXTURE_2D, self.texture)
        self.shader.set_mat4('model', model)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)


class Platform(CubeGameObject):
    LEFT = -1
    STOP = 0
    RIGHT = 1
    STEP = 0.2

    curr_movement = 0

    def __init__(self, texture_path, pos=None):
        super().__init__(texture_path, pos)

    def draw(self, move):
        if move:
            self.move()
        super().draw()

    def prep(self, shader, aspect_ratio, scale_val=None, angle=90.0):
        super().prep(shader, aspect_ratio, scale_val, angle)

    def move(self):
        if self.curr_movement == self.LEFT and self.pos[0] >= -5.0 or \
                                self.curr_movement == self.RIGHT and self.pos[0] <= 5.0:
            self.pos[0] = self.pos[0] + self.curr_movement * glfw.get_time() * self.STEP


class Background(CubeGameObject):
    scale = 11.0

    def __init__(self, texture_path):
        super().__init__(texture_path, [0.0, 5.2, 0.0])
