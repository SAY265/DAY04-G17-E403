from __future__ import annotations

import math
from typing import Any

from tools._shared import err


def calculate(expression: str = "") -> dict[str, Any]:
    """Evaluates mathematical expressions safely."""
    try:
        if not expression or not expression.strip():
            raise ValueError("Expression is empty")

        allowed_names = {
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "pow": pow,
            "sum": sum,
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "log10": math.log10,
            "pi": math.pi,
            "e": math.e,
            "ceil": math.ceil,
            "floor": math.floor,
        }

        cleaned_expr = expression.replace("^", "**").strip()
        result = eval(cleaned_expr, {"__builtins__": None}, allowed_names)
        return {"tool": "calculator", "expression": expression, "result": result}
    except Exception as exc:
        return err("calculator", exc)
