from dlin.tracer import Tracer

DEFAULTBUFFERS = {
    "corner": ["UFR", "UFL", "UBL", "UBR", "DFR", "DFL", "DBR"],
    "edge": ["UF", "UB", "UR", "UL", "FR", "FL", "DF", "DB", "DR", "DL"]
}

def trace(scramble, buffers=DEFAULTBUFFERS):
    s = Tracer(buffers)
    s.scramble_from_string(scramble)
    s.trace_cube()
    return s.tracing
