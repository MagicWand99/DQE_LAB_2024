from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

pytestmark = pytest.mark.integration

@pytest.mark.skip(reason="Google blocks automated searches (CAPTCHA/consent page), test is unstable")
def test_google_search_and_open_first_result():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    try:
        driver.get("https://www.google.com")

        if "sorry/index" in driver.current_url:
            input("CAPTCHA showed up — solve it manually, then press Enter here to continue...")

        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys("Selenium")
        search_box.send_keys(Keys.RETURN)

        first_result = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h3"))
        )
        first_result.click()

        print("Opened page:", driver.title)
        assert driver.title != ""
    finally:
        driver.quit()