from pathlib import Path
import allure
import yaml

CONFIG_DIR = Path(__file__).parent

def load_cases(file_name):
    with open(CONFIG_DIR / file_name, "r") as stream:
        return yaml.safe_load(stream)["tests"]

def run_scalar_query(cursor, sql):
    with allure.step("Run SQL query"):
        allure.attach(sql, name="SQL",
                      attachment_type=allure.attachment_type.TEXT)
        cursor.execute(sql)
        return cursor.fetchone()[0]
