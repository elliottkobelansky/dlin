#!/usr/bin/env python3

from cube.tracer import Tracer
import sys
import json


BUFFERS = {
    "corner": ["UFR", "UFL", "UBL", "UBR", "DFR", "DFL", "DBR"],
    "edge": ["UF", "UB", "UR", "UL", "FR", "FL", "DF", "DB", "DR", "DL", "BR"]
}

def dlin(scramble):
    s = Tracer(BUFFERS)
    s.scramble_from_string(scramble)
    s.trace_cube()
    return s.tracing

def main():
    if len(sys.argv) != 2:
        print("Usage: dlin [scramble]")
        sys.exit(1)
    else:
        try:
            tracing = dlin(sys.argv[1])
            sys.stdout.write(json.dumps(tracing) + "\n")
        except:
            print("Error.")
    return

if __name__ == "__main__":
    main()

