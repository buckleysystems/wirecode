from typing import List, Tuple

from wirecode import processors, plan_to_string, string_to_plan


def preprocess_gcode(plan_string: str) -> str:
    plan = string_to_plan(plan_string)
    result = processors.preprocess_integration_gcode(plan)
    return plan_to_string(result)


def label_integrals(
    plan_string: str, integrals: List[float]
) -> List[Tuple[float, float, float, float, float]]:
    plan = string_to_plan(plan_string)
    labels = processors.integral_labels(plan)
    return [
        (l[0].real, l[0].imag, l[1].real, l[1].imag, i)
        for (l, i) in zip(labels, integrals)
        if l is not None
    ]


def count_integrals_required(plan_string: str) -> int:
    plan = string_to_plan(plan_string)
    result = processors.preprocess_integration_gcode(plan)
    count_rising = len([1 for g in result if "S1000" in g.words])
    return count_rising - 1
