import allure
import pytest
from Tests.unit.db_helpers import load_cases, run_scalar_query

pytestmark = pytest.mark.unit

CASES = load_cases("config_smoke.yaml")

@allure.feature("Smoke")
@pytest.mark.smoke
@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_db_object_exists(db_cursor, case):
    allure.dynamic.title(case["name"])
    actual = run_scalar_query(db_cursor, case["sql"])
    expected = case["expected"]
    with allure.step(f"Compare actual={actual} with expected={expected}"):
        assert actual == expected, (
            f"{case['name']}: expected {expected}, got {actual}"
        )
