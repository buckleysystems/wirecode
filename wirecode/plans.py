from .geometry import p_to_z, z_to_p, unit
from .gcode import GCode
from math import e, pi, sqrt
from typing import Iterable, List


def plan_to_string(plan: Iterable[GCode]) -> str:
    return "\n".join(str(g) for g in plan)


def string_to_plan(string: str) -> List[GCode]:
    return list(GCode.from_string(line) for line in string.splitlines())


def line_plan(start, end, segments, lead_in=None, lead_out=None):
    z1 = p_to_z(start)
    z2 = p_to_z(end)
    direction = unit(z2 - z1)
    integration_length = abs(z2 - z1) / segments

    plan = []

    # Lead-in for acceleration
    if lead_in is not None:
        lead_in_pt = z1 - direction * lead_in
        plan += [GCode(["G01"]).set_position(z_to_p(lead_in_pt))]

    # Yields (segments + 1) points
    plan += [GCode(["G01"]).set_position(start)]
    for n in range(segments):
        pt = z1 + direction * integration_length * (n + 1)
        plan += [GCode(["G01"], comments=["(INT)"]).set_position(z_to_p(pt))]

    # Lead-out for deceleration
    if lead_out is not None:
        lead_out_pt = z2 + direction * lead_out
        plan += [GCode(["G01"]).set_position(z_to_p(lead_out_pt))]

    return plan


def _square_edge(quadrant, radius, segments, accel_length):
    """One edge of a square plan"""
    ext_radius = 2 * radius / sqrt(2)
    side_length = 2 * radius
    rotation = e ** (1j * pi / 2 * (quadrant - 1))
    direction = unit(-1 + 1j) * rotation
    z1 = (ext_radius + 0j) * rotation
    z2 = z1 + side_length * direction
    return line_plan(z_to_p(z1), z_to_p(z2), segments, accel_length, accel_length)


def square_plan(radius, segments_per_side, accel_length):
    sides = [
        _square_edge(q, radius, segments_per_side, accel_length) for q in (1, 2, 3, 4)
    ]
    return sum(sides, [])
