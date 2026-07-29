from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import TOOL_FUNCTIONS, load_tool_declarations
from tools.calculator.calculator import calculate


def test_calculator() -> None:
    print("--- 1. Direct function test ---")
    test_exprs = [
        "15 * 12 + sqrt(144)",
        "2^10",
        "sin(pi / 2)",
        "100 / 4",
        "invalid_func()",
    ]
    for expr in test_exprs:
        res = calculate(expr)
        print(f"calculate({expr!r}) => {res}")

    print("\n--- 2. Registration in TOOL_FUNCTIONS test ---")
    assert "calculator" in TOOL_FUNCTIONS, "calculator not found in TOOL_FUNCTIONS"
    reg_fn = TOOL_FUNCTIONS["calculator"]
    res_reg = reg_fn("5 * 5")
    print(f"TOOL_FUNCTIONS['calculator']('5 * 5') => {res_reg}")

    print("\n--- 3. Schema in tools.yaml test ---")
    declarations = load_tool_declarations(ROOT / "artifacts" / "tools.yaml")
    calc_decl = next((d for d in declarations if d["name"] == "calculator"), None)
    assert calc_decl is not None, "calculator not found in tools.yaml"
    print(f"tools.yaml declaration => {json.dumps(calc_decl, ensure_ascii=True)}")

    print("\n[SUCCESS] Quicktest for 'calculator' PASSED with 0 runtime errors!")


if __name__ == "__main__":
    test_calculator()
