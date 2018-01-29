""" Module for different helpers. Currently there is only one which is a texture loader"""
from OpenGL.GL import *
from PIL import Image
import numpy


class Textureloader:
    @staticmethod
    def load(path):
        """ takes a path to resource with texture (e.g. resources/bucket.jpg) and returns a named texture """
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)

        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # load image
        image = Image.open(path)
        img_data = numpy.array(list(image.getdata()), numpy.uint8)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

        return texture
