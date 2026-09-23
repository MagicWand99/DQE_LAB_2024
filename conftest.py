import os
import shutil
import subprocess
from pathlib import Path
import psycopg2
import pytest
import boto3
from selenium import webdriver
from moto import mock_aws

BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.fixture(scope="session")
def api_base_url():
    return BASE_URL

@pytest.fixture
def s3_client():
    with mock_aws():
        client = boto3.client("s3", region_name="us-east-1")
        client.create_bucket(Bucket="staging-bucket")
        client.put_object(
            Bucket="staging-bucket",
            Key="forecasts/2026-09-21/data.csv",
            Body=b"date,value\n2026-09-21,123",
        )
        yield client

@pytest.fixture
def gcs_bucket():
    class FakeBlob:
        def __init__(self, name):
            self.name = name

    class FakeGCSBucket:
        def __init__(self, blob_names):
            self._blobs = [FakeBlob(name) for name in blob_names]

        def list_blobs(self, prefix=None):
            if prefix:
                return [b for b in self._blobs if b.name.startswith(prefix)]
            return self._blobs

    return FakeGCSBucket(["forecasts/2026-09-21/data.csv"])

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

@pytest.fixture
def driver():                 # for the Selenium tests
    driver = webdriver.Chrome()
    yield driver
    driver.quit()
