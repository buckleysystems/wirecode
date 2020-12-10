from wirecode import plans

p1 = {"X": 1, "Y": 3}
p2 = {"X": -1, "Y": 5}

plan_gcode = "G01 X+0001.00000000 Y+0003.00000000\nG01 X+0000.33333333 Y+0003.66666667 (INT)\nG01 X-0000.33333333 Y+0004.33333333 (INT)\nG01 X-0001.00000000 Y+0005.00000000 (INT)"


def test_line_plan():
    plan = [str(g) for g in plans.line_plan(p1, p2, 3)]
    assert "\n".join(plan) == plan_gcode
