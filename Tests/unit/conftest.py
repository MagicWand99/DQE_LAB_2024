import os
import shutil
import subprocess
from pathlib import Path
import psycopg2
import pytest

# Global config
DB_CONFIG = {
    "database": os.getenv("DQ_DB_NAME", "dwh_hw_db"),
    "user": os.getenv("DQ_DB_USER", "postgres"),
    "password": os.getenv("DQ_DB_PASSWORD", "2703"),
    "host": os.getenv("DQ_DB_HOST", "localhost"),
    "port": os.getenv("DQ_DB_PORT", "5432"),
}
REPORTS_DIR = Path("allure-report")

# Fixtures
@pytest.fixture(scope="session")
def db_cursor():
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()
    yield cursor
    cursor.close()
    connection.close()

# Hooks
@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    results_dir = session.config.getoption("allure_report_dir", default=None)
    if not results_dir:
        return

    allure_cli = shutil.which("allure")
    if allure_cli is None:
        print("\nAllure CLI not found in PATH - report was not generated")
        return

    report_dir = REPORTS_DIR / Path(results_dir).name
    subprocess.run(
        [allure_cli, "generate", results_dir,
         "-o", str(report_dir), "--clean", "--single-file"],
        check=False,
    )
