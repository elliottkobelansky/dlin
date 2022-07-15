# Index with UFR, UF, etc

# Each piece has U facing, F facing, L/R facing
# Each piece belongs

# 3 tuple (U, F, R) showing D face then front then right

import cube.cube
import numpy as np

DEFAULTBUFFERS = {
    "corner": ["UFR", "UFL", "UBL", "UBR", "DFR", "DFL", "DBR"],
    "edge": ["UF", "UB", "UR", "UL", "FR", "FL", "DF", "DB", "DR", "DL"]
}

class Tracer(cube.cube.Cube):
    def __init__(self, buffers=DEFAULTBUFFERS):
        super().__init__()
        self.tracing = {"edge": [], "corner": []}
        self.buffers = buffers
        self.loopcube = []
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    self.loopcube.append((x, y, z))

    def find_piece(self, piecename):
        piecename = set(piecename)
        piece = [pos for pos in self.loopcube
                 if set(self.cube[pos].get_name()) == piecename][0]
        return piece

    def rotate_into_orientation(self):
        rotations = []
        u_center = self.find_piece("U")
        direction = max(set(u_center) - {1})
        axis = u_center.index(direction)
        if axis == 2:
            rotation = "x" if direction == 0 else "x'"
        elif axis == 0:
            rotation = "z" if direction == 0 else "z'"
        elif axis == 1:
            rotation = "z2" if direction == 0 else None
      
        if rotation:
            self.do_move(rotation)
            rotations.append(rotation)

        f_center = self.find_piece("F")
        direction = max(set(f_center) - {1})
        axis = f_center.index(direction)
        if axis == 2:
            rotation = None if direction == 0 else "y2"
        elif axis == 0:
            rotation = "y" if direction == 2 else "y'"

        if rotation:
            self.do_move(rotation)
            rotations.append(rotation)
         
        self.tracing["rotation"] = rotations

        return
  
    def edge_swap(self, a, b):
        if self.edge_orientation_adjust(a, b):
            self.edge_flip(a, b)
            
        a = self.coords_from_name(a)  
        b = self.coords_from_name(b)
        slices = a.index(1), b.index(1)
        s1, s2 = min(slices), max(slices)

        self.cube[a], self.cube[b] = self.cube[b], self.cube[a]
        
        if s1 == s2:
            pass
        elif s1 == 0:
            if s2 == 2:
                for piece in (a, b):
                    self.cube[piece].swap_stickers(0, 2)
            elif s2 == 1:
                if slices[0] == 0:
                    self.cube[a].roll(-1)
                    self.cube[b].roll(1)
                elif slices[1] == 0:
                    self.cube[a].roll(1)
                    self.cube[b].roll(-1)
        elif s1 == 1 and s2 == 2:
            for piece in (a, b):
                 self.cube[piece].swap_stickers(0, 1)
                 
        return
    
    def edge_flip(self, a, b):
        a_name, b_name = a, b
        a = self.coords_from_name(a)  
        b = self.coords_from_name(b)
        slices = a.index(1), b.index(1)
        a_1, a_2 = {0, 1, 2} - {slices[0]}
        b_1, b_2 = {0, 1, 2} - {slices[1]}
        self.cube[a].swap_stickers(a_1, a_2)
        self.cube[b].swap_stickers(b_1, b_2)
        return ({"type": "flip", "targets": [a_name, b_name]})
        
    def swap(self, a, b):
        piecetype = "edge" if len(a) == 2 else "corner"
        print(a, b)
        if piecetype == "edge":
            self.edge_swap(a, b)
        elif piecetype == "corner":
            swap_type = self.corner_swap_type(a, b)
            
        return {"type": "2-swap", "targets": [a, b]}

    def three_cycle(self, a, b, c):
        self.swap(a, b)
        self.swap(a, c)
        self.printcube()
        return {"type": "3-cycle", "targets": [a, b, c]}
        
    def edge_orientation(self, a):
        if a[0] in {"U", "D"}:
            return 0
        elif a[0] in {"F", "B"} and a[1] in {"R", "L"}:
            return 0
        else:
            return 1
    
    def edge_orientation_adjust(self, a, b):
        return 1 if self.edge_orientation(a) != self.edge_orientation(b) else 0    
    
    def coords_from_name(self, name):
        coords = [1, 1, 1]
        for side in name:
            if side == "F":
                coords[2] = 0
            elif side == "B":
                coords[2] = 2
            elif side == "U":
                coords[1] = 2
            elif side == "D":
                coords[1] = 0
            elif side == "R":
                coords[0] = 2
            elif side == "L":
                coords[0] = 0
        return tuple(coords)   
    
    def where_to(self, a):
        axis = cube.cube.FACES[a[0]]["axis"]
        piece = self.coords_from_name(a)
        return self.cube[piece].get_name(axis=axis)
    
    def set_buffer(self, target):
        self.buffer = target
        return
    
    def trace_from_target(self, target, targets=None):
        targets = targets if targets else []
        to = self.where_to(target)
        if set(list(to)) == set(list(self.buffer)):
            return
        else:
            targets.append(to)
            self.trace_from_target(to, targets)
        return targets
    
    def absolute_target(self, target):
        return set(list(target))
    
    def find_flips(self):
        flips = []
        for piece in self.loopcube:
            x, y, z = piece
            name = cube.piece.Piece(x, y, z).get_name()
            to_name = self.cube[piece].get_name()
            if 1 in piece \
            and set(list(name)) == set(list(to_name)) \
            and name != to_name:
                flips.append(name)
        return flips
    
    def find_twists(self):
        twists = []
        for piece in self.loopcube:
            x, y, z = piece
            name = cube.piece.Piece(x, y, z).get_name()
            to_name = self.cube[piece].get_name()
            if 1 not in piece \
            and set(list(name)) == set(list(to_name)) \
            and name != to_name:
                abs_target = set(list(name))
                from_sticker = name[0]
                to_sticker = to_name[0]
                
                if to_sticker in {"R", "L"} and from_sticker in {"U", "D"}:
                    ori = 1
                elif to_sticker in {"F", "B"} and from_sticker in {"U", "D"}:
                    ori = -1
                elif to_sticker in {"U", "D"} and from_sticker in {"F", "B"}:
                    ori = 1
                elif to_sticker in {"R", "L"} and from_sticker in {"F", "B"}:
                    ori = -1
                elif to_sticker in {"U", "D"} and from_sticker in {"R", "L"}:
                    ori = 1
                elif to_sticker in {"F", "B"} and from_sticker in {"R", "L"}:
                    ori = -1

                if abs_target in [{"U", "F", "R"}, {"U", "B", "L"}, {"D", "B", "R"}, {"D", "F", "L"}]:
                    ori = -ori        
                    
                twists.append({"location": name, "orientation": ori})
        return twists
                
                                                                                                   
    def edge_cycle_ori(self, targets):
        return 0 if self.where_to(targets[-1]) == self.buffer else 1

    def corner_cycle_ori(self, targets):
        last_target = self.where_to(targets[-1])
        abs_target = set(list(last_target))
        last_sticker = last_target[0]
        buffer_sticker = self.buffer[0]
        if last_target == self.buffer:
            return 0
        if last_sticker in {"R", "L"} and buffer_sticker in {"U", "D"}:
            ori = 1
        elif last_sticker in {"F", "B"} and buffer_sticker in {"U", "D"}:
            ori = -1
        elif last_sticker in {"U", "D"} and buffer_sticker in {"F", "B"}:
            ori = 1
        elif last_sticker in {"R", "L"} and buffer_sticker in {"F", "B"}:
            ori = -1
        elif last_sticker in {"U", "D"} and buffer_sticker in {"R", "L"}:
            ori = 1
        elif last_sticker in {"F", "B"} and buffer_sticker in {"R", "L"}:
            ori = -1
            
        if abs_target in [{"U", "F", "R"}, {"U", "B", "L"}, {"D", "B", "R"}, {"D", "F", "L"}]:
            ori = -ori
    
        return ori
    
    def cycle_parity(self, targets):
        return 1 if len(targets) % 2 else 0
   

    def trace_all(self, piecetype, buffers):
        solved = []
        for buffer in buffers:
            if self.absolute_target(buffer) in [self.absolute_target(x) for x in solved]:
                continue
            self.set_buffer(buffer)
            targets = self.trace_from_target(buffer)
            if targets:
                [solved.append(target) for target in targets]
                parity = self.cycle_parity(targets)
                ori = self.edge_cycle_ori(targets) if piecetype == "edge" else self.corner_cycle_ori(targets)
                self.tracing[piecetype].append({"type": "cycle", "buffer": buffer, "targets": targets, "orientation": ori, "parity": parity})

        if piecetype == "edge":
            flips = self.find_flips()
            if flips:
                for flip in flips:
                    self.tracing["edge"].append({"type": "misoriented", "location": flip, "targets": [], "orientation": 1, "parity": 0})
                    
        elif piecetype == "corner":
            twists = self.find_twists()
            if twists:
                for twist in twists:
                    self.tracing["corner"].append({"type": "misoriented", "location": twist["location"], "targets": [], "orientation": twist["orientation"], "parity": 0})

        return
    
    def modify_buffer_order(self, edgebuffers, cornerbuffers):
        self.buffers["edge"] = edgebuffers
        self.buffers["corner"] = cornerbuffers
        return

    def trace_cube(self):
        self.tracing = {"edge": [], "corner": []}
        self.rotate_into_orientation()
        self.trace_all("corner", self.buffers["corner"])
        self.trace_all("edge", self.buffers["edge"])
        return 
    
