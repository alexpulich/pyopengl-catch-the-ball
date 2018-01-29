"""
This module implements basiс objects (e.g. sphere, cube) as sets of vertices and indices
which are used for polygon meshes.
"""
import math
import numpy as np


class Sphere:
    """ Simple sphere """
    RAD = 0.5
    vertices = []
    indices = []

    def __init__(self):
        rad = self.RAD
        indices_cnt = 0

        divisions = 180
        d_theta = int(180 / divisions)
        d_lon = int(360 / divisions)
        deg_to_rad = math.pi / 180

        for lat in range(0, 181, d_theta):
            for lon in range(0, 361, d_lon):
                # Vertex1
                x = rad * math.cos(lon * deg_to_rad) * math.sin(lat * deg_to_rad)
                y = rad * math.sin(lon * deg_to_rad) * math.sin(lat * deg_to_rad)
                z = rad * math.cos(lat * deg_to_rad)
                self.vertices.append(x)
                self.vertices.append(y)
                self.vertices.append(z)
                self.vertices.append(lon / 360 - 0.25)
                self.vertices.append(lat / 180)
                self.indices.append(indices_cnt)
                indices_cnt += 1

                # vertex2
                x = rad * math.cos(lon * deg_to_rad) * math.sin((lat + d_theta) * deg_to_rad)
                y = rad * math.sin(lon * deg_to_rad) * math.sin((lat + d_theta) * deg_to_rad)
                z = rad * math.cos((lat + d_theta) * deg_to_rad)
                self.vertices.append(x)
                self.vertices.append(y)
                self.vertices.append(z)
                self.vertices.append(lon / 360 - 0.25)
                self.vertices.append((lat + d_theta - 1) / 180)
                self.indices.append(indices_cnt)
                indices_cnt += 1

                # vertex3
                x = rad * math.cos((lon + d_lon) * deg_to_rad) * math.sin(lat * deg_to_rad)
                y = rad * math.sin((lon + d_lon) * deg_to_rad) * math.sin(lat * deg_to_rad)
                z = rad * math.cos(lat * deg_to_rad)
                self.vertices.append(x)
                self.vertices.append(y)
                self.vertices.append(z)
                self.vertices.append((lon + d_lon) / 360 - 0.25)
                self.vertices.append(lat / 180)
                self.indices.append(indices_cnt)
                indices_cnt += 1

                # vertex4
                x = rad * math.cos((lon + d_lon) * deg_to_rad) * math.sin((lat + d_theta) * deg_to_rad)
                y = rad * math.sin((lon + d_lon) * deg_to_rad) * math.sin((lat + d_theta) * deg_to_rad)
                z = rad * math.cos((lat + d_theta) * deg_to_rad)
                self.vertices.append(x)
                self.vertices.append(y)
                self.vertices.append(z)
                self.vertices.append((lon + d_lon) / 360 - 0.25)
                self.vertices.append((lat + d_theta) / 180)
                self.indices.append(indices_cnt)
                indices_cnt += 1

        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.indices = np.array(self.indices, dtype=np.uint32)


class Cube:
    """ Simple cube """

    def __init__(self):
        self.vertices = np.array([
            # format: x, y, z, texture_x, texture_y
            -0.5, -0.5, 0.5, 0.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, -0.5, 1.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            -0.5, 0.5, -0.5, 0.0, 1.0,

            0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            0.5, -0.5, 0.5, 0.0, 1.0,

            -0.5, 0.5, -0.5, 0.0, 0.0,
            -0.5, -0.5, -0.5, 1.0, 0.0,
            -0.5, -0.5, 0.5, 1.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, -0.5, 1.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 1.0,
            -0.5, -0.5, 0.5, 0.0, 1.0,

            0.5, 0.5, -0.5, 0.0, 0.0,
            -0.5, 0.5, -0.5, 1.0, 0.0,
            -0.5, 0.5, 0.5, 1.0, 1.0,
            0.5, 0.5, 0.5, 0.0, 1.0
        ], dtype=np.float32)

        self.indices = np.array([
            0, 1, 2, 2, 3, 0,
            4, 5, 6, 6, 7, 4,
            8, 9, 10, 10, 11, 8,
            12, 13, 14, 14, 15, 12,
            16, 17, 18, 18, 19, 16,
            20, 21, 22, 22, 23, 20
        ], dtype=np.uint32)


class Heart:
    """ Simple rough heart """

    def __init__(self):
        self.vertices = np.array([
            # format: x, y, z
            0.0, -0.8, 0.0,

            -0.6, 0.1, 0.0,
            -0.3, 0.6, 0.0,

            0.0, 0.4, 0.0,

            0.3, 0.6, 0.0,
            0.6, 0.1, 0.0
        ], dtype=np.float32)

        self.indices = np.array([
            0, 1, 2,
            2, 0, 3,
            3, 4, 0,
            0, 5, 4,
        ], dtype=np.uint32)
