import unittest
import numpy as np

from primitives import Sphere, Cube, Heart


class PrimitivesTest(unittest.TestCase):

    def test_create_sphere(self):
        sphere = Sphere()
        self.assertIsInstance(sphere.vertices, np.ndarray, "Vertices is not an instance of numpy.ndarray")
        self.assertIsInstance(sphere.indices, np.ndarray, "Indices is not an instance of numpy.ndarray")
        self.assertIs(sphere.vertices.dtype.type, np.float32, "Numpy array's elements are not numpy.float32")
        self.assertIs(sphere.indices.dtype.type, np.uint32, "Numpy array's elements are not numpy.uint32")
        self.assertGreater(len(sphere.vertices), 0, "Sphere does not have any vertices")
        self.assertGreater(len(sphere.indices), 0, "Sphere does not have any indices for vertices")

    def test_create_cube(self):
        cube = Cube()
        self.assertIsInstance(cube.vertices, np.ndarray, "Vertices is not an instance of numpy.ndarray")
        self.assertIsInstance(cube.indices, np.ndarray, "Indices is not an instance of numpy.ndarray")
        self.assertIs(cube.vertices.dtype.type, np.float32, "Numpy array's elements are not numpy.float32")
        self.assertIs(cube.indices.dtype.type, np.uint32, "Numpy array's elements are not numpy.uint32")
        self.assertGreater(len(cube.vertices), 0, "Cube does not have any vertices")
        self.assertGreater(len(cube.indices), 0, "Cube does not have any indices for vertices")

    def test_create_heart(self):
        heart = Heart()
        self.assertIsInstance(heart.vertices, np.ndarray, "Vertices is not an instance of numpy.ndarray")
        self.assertIsInstance(heart.indices, np.ndarray, "Indices is not an instance of numpy.ndarray")
        self.assertIs(heart.vertices.dtype.type, np.float32, "Numpy array's elements are not numpy.float32")
        self.assertIs(heart.indices.dtype.type, np.uint32, "Numpy array's elements are not numpy.uint32")
        self.assertGreater(len(heart.vertices), 0, "Heart does not have any vertices")
        self.assertGreater(len(heart.indices), 0, "Heart does not have any indices for vertices")


if __name__ == '__main__':
    unittest.main()
