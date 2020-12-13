from typing import List
from .gcode import GCode, split_line
from .geometry import p
from .tools import iter_with_lookahead


def preprocess_integration_gcode(gcode: List[GCode]) -> List[GCode]:
    position = p(0, 0)
    gcode_out = []
    for line, next_line in iter_with_lookahead(gcode):
        g_line = line.copy()
        this_int = "(INT)" in line.comments
        next_int = "(INT)" in next_line.comments
        # Add comment if this is start or end of segment
        if this_int and not next_int:
            g_line.comments += ["(START)"]
        if next_int and not this_int:
            g_line.comments += ["(END)"]
        # Split if needed
        if this_int or next_int:
            (g_mid,) = split_line(position, line)
            g_mid.words += ["S1000"]
            g_line.words += ["S0000"]
            gcode_out += [g_mid, g_line]
        else:
            gcode_out += [line]
        # Keep track of current position
        position.update(line.get_position())
    return gcode_out
