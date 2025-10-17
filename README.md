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

### Basic Usage:
```python
from dlin import trace
scr = "F' L2 B2 F2 D' F2 D F2 U R2 U' L' B L' R' F2 R2 B2 U2 Fw'"
described_cycles = trace(scr)
```

### Parameters:

#### `buffers`: dict, optional

Defines the buffer order for tracing. Must in format `{"corner": [...], "edge": [...]}`. The `corner` and `edge` lists can each be permuted as desired. The default is the standard canonical buffer ordering:

```
DEFAULTBUFFERS = {
    "corner": ["UFR", "UFL", "UBL", "UBR", "DFR", "DFL", "DBR", "DBL"],
    "edge": ["UF", "UB", "UR", "UL", "FR", "FL", "DF", "DB", "DR", "DL", "BR", "BL"]
}
```

#### `trace`: str, optional

Specifies which pieces to trace. Options:
- `"both"`: trace both edges and corners (default)
- `"edges"`: trace only edges
- `"corners"`: trace only corners

#### `swap`: tuple, optional

Pseudoswap (pre-swap) two edges before tracing. Only stickers on EO axis are currently supported (i.e. any piece in `DEFAULTBUFFERS["edge"]`).

Format: `(e1, e2)`

Example: `swap=("UF", "UR")` swaps UF-UR.

### Example Output

Here is what would be contained in `described_cycles`
```python
{
  "edge": [
    {
      "type": "cycle",
      "buffer": "UF",
      "targets": [
        "LD",
        "LF",
        "RU",
        "LU"
      ],
      "orientation": 0,
      "parity": 0
    },
    {
      "type": "cycle",
      "buffer": "UB",
      "targets": [
        "RB",
        "DR"
      ],
      "orientation": 1,
      "parity": 0
    },
    {
      "type": "cycle",
      "buffer": "FR",
      "targets": [
        "DB",
        "DF"
      ],
      "orientation": 1,
      "parity": 0
    }
  ],
  "corner": [
    {
      "type": "cycle",
      "buffer": "UFR",
      "targets": [
        "UBL",
        "RUB",
        "RDB",
        "FDR",
        "UFL",
        "FDL"
      ],
      "orientation": 1,
      "parity": 0
    },
    {
      "type": "misoriented",
      "buffer": "DBL",
      "targets": [],
      "orientation": -1,
      "parity": 0
    }
  ],
  "scramble": "F' L2 B2 F2 D' F2 D F2 U R2 U' L' B L' R' F2 R2 B2 U2 Fw'",
  "rotation": [
    "z"
  ],
  "edge_cc": "5e3e'3e'",
  "corner_cc": "7c'1t"
}
```




## Usage: Command Line Script
Run 
```
dlin-trace [scramble]
```
Make sure to surround the scramble in quotation marks. This will output a json, 
with similar structure to the dictionary shown above. Buffer order and swap can be manually updated by editing the `dlin-trace` script.

