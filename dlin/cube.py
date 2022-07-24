import dlin.piece
import numpy as np

FACES = {
    "L": {"axis": 0, "pos": 0},
    "M": {"axis": 0, "pos": 1},
    "R": {"axis": 0, "pos": 2},
    "F": {"axis": 2, "pos": 0},
    "S": {"axis": 2, "pos": 1},
    "B": {"axis": 2, "pos": 2},
    "U": {"axis": 1, "pos": 2},
    "E": {"axis": 1, "pos": 1},
    "D": {"axis": 1, "pos": 0}
}

class Cube():
    def __init__(self):
        self.cube = np.ndarray((3, 3, 3), dtype=dlin.piece.Piece)
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    self.cube[x, y, z] = dlin.piece.Piece(x, y, z)

        self.solved = np.copy(self.cube)
        self.scramble = ""

    def reset_cube_to_solved(self):
        self.cube = self.solved
        return

    def single_turn(self, face, clockwise=True):
        k = 1 if clockwise else -1
        k = -k if face in {"U", "L", "F", "S", "M"} else k
        axis, pos = FACES[face].values()
        index = [slice(None), slice(None), slice(None)]
        index[axis] = pos
        index = tuple(index)
        self.cube[index] = np.rot90(self.cube[index], k)
        axis1, axis2 = {0, 1, 2} - {axis}
        for piece in self.cube[index].flatten():
            piece.swap_stickers(axis1, axis2)
        return

    def wide_turn(self, face, clockwise=True):
        sliceclockwise = clockwise
        if face in {"R", "U", "B"}:
            sliceclockwise = not clockwise
        if face in {"L", "R"}:
            sliceface = "M"
        elif face in {"U", "D"}:
            sliceface = "E"
        elif face in {"F", "B"}:
            sliceface = "S"
        self.single_turn(face, clockwise)
        self.single_turn(sliceface, sliceclockwise)
        return

    def rotation(self, rotation, clockwise=True):
        axis = rotation[0]
        if axis == "x":
            moves = ["R", "M'", "L'"]
        elif axis == "y":
            moves = ["U", "E'", "D'"]
        elif axis == "z":
            moves = ["F", "S", "B'"]
        
        if not clockwise:
            [[self.do_move(move) for move in moves] for i in range(3)]
        else:
            [self.do_move(move) for move in moves]
        return

    def do_move(self, move):
        clockwise = False if "'" in move else True
        face = move[0]
        turn = lambda x: self.single_turn(face, clockwise)
        if "x" in move or "y" in move or "z" in move:
            turn = lambda x: self.rotation(face, clockwise)
        if "w" in move:
            turn = lambda x: self.wide_turn(face, clockwise)
        if "2" in move:
            turn(face)
            turn(face)
        else:
            turn(face)
        return

    def scramble_from_string(self, scram):
        self.scramble = scram
        moves = scram.split(" ")
        for move in moves:
            self.do_move(move)
        return
