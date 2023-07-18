from dlin.tracer import Tracer

def trace(scramble, pseudoswap=None):
    s = Tracer()
    if pseudoswap:
        e1, e2 = pseudoswap
        s.pseudoswap(e1, e2)
    s.scramble_from_string(scramble)
    s.trace_cube()
    return s.tracing
