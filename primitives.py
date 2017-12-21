import math
import numpy as np


class Sphere:

    RAD = 0.5
    vertices = []
    indices = []

    def __init__(self):
        rad = self.RAD
        indicesCnt = 0

        divisions = 180
        dTheta = int(180 / divisions)
        dLon = int(360 / divisions)
        degToRad = math.pi / 180

        for lat in range(0, 181, dTheta):
            for lon in range(0, 361, dLon):
                # Vertex1
                x = rad * math.cos(lon * degToRad) * math.sin(lat * degToRad)
                y = rad * math.sin(lon * degToRad) * math.sin(lat * degToRad)
                z = rad * math.cos(lat * degToRad)
                self.vertices.append(x)
                self.vertices.append(y)
                self.vertices.append(z)
                self.vertices.append(lon / 360 - 0.25)
                self.vertices.append(lat / 180)
                self.indices.append(indicesCnt)
                indicesCnt += 1

                # vertex2
                x = rad * math.cos(lon * degToRad) * math.sin((lat + dTheta) * degToRad)
                y = rad * math.sin(lon * degToRad) * math.sin((lat + dTheta) * degToRad)
                z = rad * math.cos((lat + dTheta) * degToRad)
                self.vertices.append(x)
                self.vertices.append(y)
                self.vertices.append(z)
                self.vertices.append(lon / 360 - 0.25)
                self.vertices.append((lat + dTheta - 1) / 180)
                self.indices.append(indicesCnt)
                indicesCnt += 1
                # vertex3
                x = rad * math.cos((lon + dLon) * degToRad) * math.sin(lat * degToRad)
                y = rad * math.sin((lon + dLon) * degToRad) * math.sin(lat * degToRad)
                z = rad * math.cos(lat * degToRad)
                self.vertices.append(x)
                self.vertices.append(y)
                self.vertices.append(z)
                self.vertices.append((lon + dLon) / 360 - 0.25)
                self.vertices.append(lat / 180)
                self.indices.append(indicesCnt)
                indicesCnt += 1

                # vertex4
                x = rad * math.cos((lon + dLon) * degToRad) * math.sin((lat + dTheta) * degToRad)
                y = rad * math.sin((lon + dLon) * degToRad) * math.sin((lat + dTheta) * degToRad)
                z = rad * math.cos((lat + dTheta) * degToRad)
                self.vertices.append(x)
                self.vertices.append(y)
                self.vertices.append(z)
                self.vertices.append((lon + dLon) / 360 - 0.25)
                self.vertices.append((lat + dTheta) / 180)
                self.indices.append(indicesCnt)
                indicesCnt += 1

        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.indices = np.array(self.indices, dtype=np.uint32)


class Cube:
    def __init__(self):
        self.vertices = np.array([
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