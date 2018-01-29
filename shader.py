from OpenGL.GL import *
from OpenGL.GL.shaders import *


class Shader:
    """ Wrapper for simple work with shaders """

    def __init__(self, vertex_shader, fragment_shader):
        """ Compiles shader and saves its id on Shader object creating """
        self.id = self._compile_shader(vertex_shader, fragment_shader)

    def use(self):
        """ Simple wrapper for glUseProgram. Installs a program object as part of current rendering state"""
        glUseProgram(self.id)

    def set_mat4(self, param, value):
        """ Specifies the value of a uniform variable <param> for the current program object """
        location = glGetUniformLocation(self.id, param)
        glUniformMatrix4fv(location, 1, GL_FALSE, value)

    def _load_shader(self, shader_file):
        """ Reads shader program from text file """
        with open(shader_file) as f:
            shader_source = f.read()
        return str.encode(shader_source)

    def _compile_shader(self, vertex_shader, fragment_shader):
        """ Compiles shader programs and returns """
        vertex_shader = self._load_shader(vertex_shader)
        fragment_shader = self._load_shader(fragment_shader)

        shader = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
        )

        return shader
