from OpenGL.GL import *
from OpenGL.GL.shaders import *

class Shader:

    def __init__(self, vertex_shader, fragment_shader):
        self.id = self._compile_shader(vertex_shader, fragment_shader)

    def use(self):
        glUseProgram(self.id)

    def setMat4(self, name, value):
        location = glGetUniformLocation(self.id, name)
        glUniformMatrix4fv(location, 1, GL_FALSE, value)

    def setMat4(self, name, value):
        location = glGetUniformLocation(self.id, name)
        glUniformMatrix4fv(location, 1, GL_FALSE, value)

    def _load_shader(self, shader_file):
        shader_source = ''
        with open(shader_file) as f:
            shader_source = f.read()
        return str.encode(shader_source)

    def _compile_shader(self, vertex_shader, fragment_shader):
        vertex_shader = self._load_shader(vertex_shader)
        fragment_shader = self._load_shader(fragment_shader)

        shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                                  OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

        return shader