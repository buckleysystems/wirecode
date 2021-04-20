from .geometry import p_to_z, z_to_p, unit, p
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

def circle_plan(radius, number_segments, lead_in_deg=45, lead_out_deg=45):
    segment_angle = 2*pi/number_segments
    # Start offset by half a segment so that the midpoint is at 0
    start_angle = -segment_angle/2

    # Calculate number of segments in the lead-in
    #Approximately the same angular frequency as the main circle
    lead_in_angle = -pi*lead_in_deg/180
    lead_in_segments = round((start_angle-lead_in_angle)/segment_angle)
    lead_in_segment_angle = (start_angle-lead_in_angle)/lead_in_segments

    # Same for lead-out
    lead_out_angle = pi*lead_out_deg/180
    lead_out_segments = round((lead_out_angle - start_angle)/segment_angle)
    lead_out_segment_angle = (lead_out_angle - start_angle)/lead_out_segments

    plan = []
    
    # Do the lead-in
    for n in range(lead_in_segments+1):
        next_angle = lead_in_angle + n*lead_in_segment_angle
        next_point = radius*e**(1j*next_angle)
        plan += [GCode(["G01"]).set_position(z_to_p(next_point))]
    
    # Do the integrals
    for n in range(number_segments):
        next_angle = start_angle + (n+1)*segment_angle
        next_point = radius*e**(1j*next_angle)
        plan += [GCode(["G01"], comments=["(INT)"]).set_position(z_to_p(next_point))]
    
    # Do the lead-out
    for n in range(lead_out_segments):
        next_angle = start_angle + (n+1)*lead_out_segment_angle
        next_point = radius*e**(1j*next_angle)
        plan += [GCode(["G01"]).set_position(z_to_p(next_point))]

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


def square_plan(
    radius: float, segments_per_side: int, accel_length: float
) -> List[GCode]:
    sides = [
        _square_edge(q, radius, segments_per_side, accel_length) for q in (1, 2, 3, 4)
    ]
    return sum(sides, [])


def plan_to_coordinates(plan: List[GCode]) -> List[complex]:
    """Returns all coordinates in plan
    
    includes points not involved in integration"""
    position = p(0, 0)
    coordinates: List[complex] = []
    for g in plan:
        old_position = position.copy()
        position.update(g.get_position())
        if position != old_position:
            coordinates.append(p_to_z(position))
    return coordinates
