# dlin
Describe piece cycles on a Rubik's Cube.

## Installing
To install, run
```
pip install dlin
```
## Usage: As a Python Package
The `dlin.trace` function converts a scramble
(set of moves defined by [WCA regulation 12a](https://www.worldcubeassociation.org/regulations/#12a) separated by spaces)
into a python dictionary describing cycles on the cube. 

To use, run
```python
from dlin import trace
```
The following is example code to get the tracing for a scramble.
```python
described_cycles = trace("F' L2 B2 F2 D' F2 D F2 U R2 U' L' B L' R' F2 R2 B2 U2 Fw'")
```
Here is an example of what could be contained in `described_cycles`
```python
{
    "edge": [
        {
            "type": "cycle",
            "buffer": "UF",
            "targets": ["LD", "LF", "RU", "LU"],
            "orientation": 0,
            "parity": 0,
        },
        {
            "type": "cycle",
            "buffer": "UB",
            "targets": ["RB", "DR"],
            "orientation": 1,
            "parity": 0,
        },
        {
            "type": "cycle",
            "buffer": "FR",
            "targets": ["DB", "DF"],
            "orientation": 1,
            "parity": 0,
        },
    ],
    "corner": [
        {
            "type": "cycle",
            "buffer": "UFR",
            "targets": ["UBL", "RUB", "RDB", "FDR", "UFL", "FDL"],
            "orientation": 1,
            "parity": 0,
        },
        {
            "type": "misoriented",
            "buffer": "DBL",
            "targets": [],
            "orientation": -1,
            "parity": 0,
        },
    ],
    "scramble": "F' L2 B2 F2 D' F2 D F2 U R2 U' L' B L' R' F2 R2 B2 U2 Fw'",
    "rotation": ["z"],
}
```
## Usage: Command Line Script
Run 
```
dlin-trace [scramble]
```
Make sure to surround the scramble in quotation marks. This will output a json, 
with similar structure to the dictionary shown above.

