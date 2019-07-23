import math
import ctypes
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

class Bone():
    def __init__(self):
        #type (Name) of bone: String
        self.bone_type = None
        
        #3D model definitions of outer bounding box: Float
        self.length = None
        self.width = None
        self.height = None

        #Volume is calculated by the type and dimenstions: Float
        self.volume = None

        self.vertices=()
        self.edges=()

    def create(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()
class Skull(Bone):
    def __init__(self):
        bone_type = "Skull"


class Longbone(Bone):
    def __init__(self):
        bone_type = "Longbone"
        self.vertices=(
            (1,-1,-1),
            (1,1,-1),
            (-1,1,-1),
            (-1,-1,-1),
            (0,0,5)
        )
        self.edges=(
            (0,1), (0,3),
            (0,4), (1,4),
            (1,2), (2,4),
            (2,3), (3,4)
        )

class Tail(Bone):
    def __init__(self):
        pass

if __name__ == "__main__":
    pygame.init()
    display=(800,800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50)
    
    glTranslatef(0.0,0.0,-20)
    glRotatef(90.0, -1, 0, 0)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glRotatef(0.1, 1, 0, 0)
        bone = Longbone()
        bone.create()
        pygame.display.flip()