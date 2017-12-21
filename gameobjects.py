from OpenGL.GL import *
import numpy as np
from utils import Textureloader
from pyrr import matrix44, matrix33, Vector3
import glfw
import random
from primitives import Cube, Sphere


class SphereGameObject(Sphere):
    VAO = None
    VBO = None
    EBO = None

    pos = [2.0, 0.0, 0.0]
    scale = 0.5

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
            self.texture = Textureloader.load_texture(texture_path)

        if pos:
            self.pos = pos

    def prep(self, shader, aspect_ratio, scale_val=None, angle=90.0):
        print(aspect_ratio)
        self.shader = shader
        self.shader.use()

        if scale_val:
            self.scale = scale_val

        view = matrix44.create_from_translation(Vector3([0.0, -2.5, -8.0]))
        self.shader.setMat4('view', view)

        projection = matrix44.create_perspective_projection_matrix(angle, aspect_ratio, 0.1, 100.0)
        self.shader.setMat4('projection', projection)

        scale = matrix33.create_from_scale(Vector3([self.scale, self.scale, self.scale]))
        scale = matrix44.create_from_matrix33(scale)
        self.shader.setMat4('scale', scale)

    def draw(self):
        self.shader.use()

        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)

        model = matrix44.create_from_translation(Vector3(self.pos))
        glBindTexture(GL_TEXTURE_2D, self.texture)
        self.shader.setMat4('model', model)
        glDrawElements(GL_LINE_LOOP, len(self.indices), GL_UNSIGNED_INT, None)


class Ball(SphereGameObject):

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
        self.pos[1] = self.pos[1] - self.speed


class Heart:
    scale = 1.0
    shader = None

    def __init__(self, pos):
        self.vertices = []
        self.indices = []
        self.pos = pos
        self.vertices = [
            0.0, -0.8, 0.0,

            -0.6, 0.1, 0.0,
            -0.3, 0.6, 0.0,

            0.0, 0.4, 0.0,

            0.3, 0.6, 0.0,
            0.6, 0.1, 0.0
        ]
        self.indices = [
            0, 1, 2,
            2, 0, 3,
            3, 4, 0,
            0, 5, 4,
        ]
        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.indices = np.array(self.indices, dtype=np.uint32)

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

        view = matrix44.create_from_translation(Vector3([0.0, -2.5, -8.0]))
        self.shader.setMat4('view', view)

        projection = matrix44.create_perspective_projection_matrix(angle, aspect_ratio, 0.1, 100.0)
        self.shader.setMat4('projection', projection)

        scale = matrix33.create_from_scale(Vector3([self.scale, self.scale, self.scale]))
        scale = matrix44.create_from_matrix33(scale)
        self.shader.setMat4('scale', scale)

    def draw(self):
        self.shader.use()
        glBindVertexArray(self.VAO)
        glEnable(GL_PRIMITIVE_RESTART)
        glPrimitiveRestartIndex(GL_PRIMITIVE_RESTART_FIXED_INDEX)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)

        model = matrix44.create_from_translation(Vector3(self.pos))
        self.shader.setMat4('model', model)
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
            self.texture = Textureloader.load_texture(texture_path)

        if pos:
            self.pos = pos

    def prep(self, shader, aspect_ratio, scale_val=None, angle=90.0):
        self.shader = shader
        self.shader.use()

        if scale_val:
            self.scale = scale_val

        view = matrix44.create_from_translation(Vector3([0.0, -2.5, -8.0]))
        self.shader.setMat4('view', view)

        projection = matrix44.create_perspective_projection_matrix(angle, aspect_ratio, 0.1, 100.0)
        self.shader.setMat4('projection', projection)

        scale = matrix33.create_from_scale(Vector3([self.scale, self.scale, self.scale]))
        scale = matrix44.create_from_matrix33(scale)
        self.shader.setMat4('scale', scale)

    def draw(self):
        self.shader.use()

        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)

        model = matrix44.create_from_translation(Vector3(self.pos))
        glBindTexture(GL_TEXTURE_2D, self.texture)
        self.shader.setMat4('model', model)
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


class Item(CubeGameObject):
    INITIAL_SPEED = 0.02
    speed = INITIAL_SPEED

    def __init__(self, texture_path):
        super().__init__(texture_path, self.random_pos())

    def random_pos(self):
        self.pos = [random.uniform(-5, 5), 6.1, 0.0]

    def draw(self, move=True):
        if move:
            self.move()
        super().draw()

    def move(self):
        self.pos[1] = self.pos[1] - self.speed


class Background(CubeGameObject):
    scale = 11.0

    def __init__(self, texture_path):
        super().__init__(texture_path, [0.0, 5.2, 0.0])
