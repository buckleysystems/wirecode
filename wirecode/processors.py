from typing import List, Tuple, Optional
from .gcode import GCode, split_line
from .geometry import p, p_to_z
from .tools import iter_with_lookbehind, iter_with_lookahead


def preprocess_integration_gcode(gcode: List[GCode]) -> List[GCode]:
    position = p(0, 0)
    gcode_out = []
    for last_line, this_line in iter_with_lookbehind(gcode, fillvalue=GCode()):
        # Check where we are
        last_int = "(INT)" in last_line.comments
        this_int = "(INT)" in this_line.comments
        # Copy line to modify if needed
        g_line = this_line.copy()
        if this_int:
            g_line.comments.remove("(INT)")
        # Split if needed
        if last_int or this_int:
            (g_mid,) = split_line(position, g_line)
            g_mid.words += ["S1000"]
            g_line.words += ["S0000"]
            gcode_out += [g_mid, g_line]
        else:
            gcode_out += [g_line]
        # Keep track of current position
        position.update(g_line.get_position())
    return gcode_out


def integral_labels(gcode: List[GCode]) -> List[Optional[Tuple[complex, complex]]]:
    position = p(0, 0)
    positions: List[Optional[Tuple[complex, complex]]] = []
    for line, next_line in iter_with_lookahead(gcode, GCode()):
        next_position = position.copy()
        next_position.update(line.get_position())
        if "(INT)" in line.comments:
            positions += [(p_to_z(position), p_to_z(next_position))]
            if "(INT)" not in next_line.comments:
                positions += [None]
        position = next_position
    return positions[:-1]
