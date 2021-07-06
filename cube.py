import pygame
from numpy import array
from math import cos, sin


X, Y, Z = 0, 1, 2


def r_m(a, b, c):
    return (
        (cos(b)*cos(c), -cos(b)*sin(c), sin(b)),
        (cos(a)*sin(c) + sin(a)*sin(b)*cos(c), cos(a)*cos(c) - sin(c)*sin(a)*sin(b), -cos(b)*sin(a)),
        (sin(c)*sin(a) - cos(a)*sin(b)*cos(c), cos(a)*sin(c)*sin(b) + sin(a)*cos(c), cos(a)*cos(b))
    )


class PhysicalBody:
    def __init__(self, vertices, edges):
        """
        a 3D object that can rotate around the three axes
        :param vertices: a tuple of points (each has 3 coordinates)
        :param edges: a tuple of pairs (each pair is a set containing 2 vertices' indexes)
        """
        self.__vertices = array(vertices)
        self.__edges = tuple(edges)
        self.__rotation = [0, 0, 0]  # radians around each axis

    def rotate(self, axis, θ):
        self.__rotation[axis] += θ

    @property
    def lines(self):
        location = self.__vertices.dot(r_m(*self.__rotation))  # an index->location mapping
        return ((location[v1], location[v2]) for v1, v2 in self.__edges)

BLACK, RED = (0, 0, 0), (255,99,71)


class Paint:
    def __init__(self, shape, keys_handler):
        self.__shape = shape
        self.__keys_handler = keys_handler
        self.__size = 900, 900
        self.__clock = pygame.time.Clock()
        self.__screen = pygame.display.set_mode(self.__size)
        self.__mainloop()

    def __fit(self, vec):
        # notice that len(self.__size) is 2, hence zip(vec, self.__size) ignores the vector's last coordinate
        return [round(70 * coordinate + frame / 2) for coordinate, frame in zip(vec, self.__size)]

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        self.__keys_handler(pygame.key.get_pressed())

    def __draw_shape(self, thickness=5):
        for start, end in self.__shape.lines:
            pygame.draw.line(self.__screen, (abs(start[0]*30+0.3*end[0]*100),abs(end[0]*120*0.6 - 117*0.4*start[0]),abs(0.2*145*end[0])), self.__fit(start), self.__fit(end), thickness)
    def __mainloop(self):
        while True:
            self.__handle_events()
            self.__screen.fill(BLACK)
            self.__draw_shape()
            pygame.display.flip()
            self.__clock.tick(9000)

def main():
    from pygame import K_q, K_w, K_a, K_s, K_z, K_x

    cube = PhysicalBody(  # 0         1            2       3              4          5          6            7             8       9      
        vertices=((2, 2, 1.6), (2, 2, -2),(2, -2, 2), (2, -2, -2), (-2, 2, 2), (-2, 2, -2), (-2, -2, 2), (-2, -2, -2),(2,1.6,2),(1.6,2,2)),
        edges=({0,1},{0,9},{0,8},{1,3},{3,2},{2,8},{8,9},{1,5},{5,4},{4,9},{4,6},{6,7},{7,5},{7,3},{6,2})
    )


    counter_clockwise = 0.005  # radians
    clockwise = -counter_clockwise

    params = {
        K_q: (X, clockwise),
        K_w: (X, counter_clockwise),
        K_a: (Y, clockwise),
        K_s: (Y, counter_clockwise),
        K_z: (Z, clockwise),
        K_x: (Z, counter_clockwise),
    }

    def keys_handler(keys):
        for key in params:
            if keys[key]:
                cube.rotate(*params[key])

    pygame.init()
    programIcon = pygame.image.load('sugar-cubes.png')
    pygame.display.set_icon(programIcon)
    pygame.display.set_caption('Control -   q,w : X    a,s : Y    z,x : Z')
    Paint(cube, keys_handler)

if __name__ == '__main__':
    main()
