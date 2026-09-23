from pathlib import Path
import pytest
import yaml

pytestmark = pytest.mark.unit

CONFIG_PATH = Path(__file__).parent / "config.yaml"

def get_numbers_data(config_name):
    with open(config_name, "r") as stream:
        config = yaml.safe_load(stream)
    return config["cases"]

def add_numbers(a, b, c):
    try:
        return a + b + c
    except TypeError:
        raise TypeError(
            "Please check the parameters. All of them must be numeric"
        )

CASES = get_numbers_data(CONFIG_PATH)

@pytest.mark.smoke
@pytest.mark.parametrize(
    "case",
    CASES,
    ids=[case["case_name"] for case in CASES],
)
def test_add_numbers(case):
    a, b, c = case["input"]
    result = add_numbers(a, b, c)
    assert result == case["expected"], (
        f"Expected {case['expected']}, got {result}"
    )

@pytest.mark.critical
def test_add_invalid_types():
    with pytest.raises(TypeError):
        add_numbers("a", 2, 1)
