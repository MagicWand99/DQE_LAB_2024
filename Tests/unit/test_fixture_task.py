import time
import pytest

pytestmark = pytest.mark.unit

@pytest.fixture(scope="session", autouse=True)
def track_suite_time():
# Measure the whole suite. session scope + autouse => runs once.
    start = time.time()
    yield
    duration = time.time() - start
    print(f"\n[suite] Whole suite took {duration:.2f} s")

@pytest.fixture()
def track_test_time():
# Measure one test. Default (function) scope => runs for each test.
    start = time.time()
    yield
    duration = time.time() - start
    print(f"\n[test] Test took {duration:.2f} s")

def add_numbers(a, b):
    return a + b

def test_add_two_positive_numbers(track_test_time):
    a, b = 3, 5
    result = add_numbers(a, b)
    time.sleep(2)
    assert result == 8, f"Expected 8, got {result}"

def test_add_two_negative_numbers(track_test_time):
    a, b = -3, -5
    result = add_numbers(a, b)
    time.sleep(3)
    assert result == -8, f"Expected -8, got {result}"

def test_add_negative_and_positive_numbers():
# The last test intentionally does NOT use track_test_time
    a, b = -3, 5
    result = add_numbers(a, b)
    time.sleep(10)
    assert result == 2, f"Expected 2, got {result}"
