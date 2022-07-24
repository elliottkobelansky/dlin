import numpy as np

class Piece():
    def __init__(self, x, y, z):
        xd = {0: "L", 1: "", 2: "R"}
        yd = {0: "D", 1: "", 2: "U"}
        zd = {0: "F", 1: "", 2: "B"}
        self.sides = [xd[x], yd[y], zd[z]]

    def get_name(self, axis=1):
        face_precedence = {"U": 0, "D": 0, "F": 1, "B": 1, "R": 2, "L": 2, "": 3}
        axis_face = self.sides[axis]
        axis_face = self.sides[2] if not axis_face else axis_face
        name = self.sides.copy()
        index = name.index(axis_face)
        name[index], name[0] = name[0], name[index]
        name[1:] = sorted(name[1:], key=lambda x: face_precedence[x])
        return "".join(name)
                
    def swap_stickers(self, axis1, axis2):
        self.sides[axis1], self.sides[axis2] = self.sides[axis2], self.sides[axis1]
        return
    
    def roll(self, k):
        self.sides = np.roll(self.sides, k)
        return
