from .geometry import p_to_z, z_to_p, unit
from .gcode import GCode


def line_plan(start, end, segments, lead_in=None, lead_out=None):
    z1 = p_to_z(start)
    z2 = p_to_z(end)
    direction = unit(z2 - z1)
    integration_length = abs(z2 - z1) / segments

    # Lead-in for acceleration
    if lead_in is not None:
        lead_in_pt = z1 - direction * lead_in
        yield GCode(["G01"]).set_position(z_to_p(lead_in_pt))

    # Yields (segments + 1) points
    yield GCode(["G01"]).set_position(start)
    for n in range(segments):
        pt = z1 + direction * integration_length * (n + 1)
        yield GCode(["G01"], comments=["(INT)"]).set_position(z_to_p(pt))

    # Lead-out for deceleration
    if lead_out is not None:
        lead_out_pt = z2 + direction * lead_out
        yield GCode(["G01"]).set_position(z_to_p(lead_out_pt))
