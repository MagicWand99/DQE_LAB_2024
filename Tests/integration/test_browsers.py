from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
import pytest

pytestmark = pytest.mark.integration

def test_chrome_and_firefox_titles():
    chrome_driver = webdriver.Chrome()
    chrome_driver.get("https://www.google.com")
    print("Chrome page title:", chrome_driver.title)
    assert chrome_driver.title != ""
    chrome_driver.quit()

    firefox_service = FirefoxService(executable_path=r"C:\webdrivers\geckodriver.exe")
    firefox_driver = webdriver.Firefox(service=firefox_service)
    firefox_driver.get("https://www.google.com")
    print("Firefox page title:", firefox_driver.title)
    assert firefox_driver.title != ""
    firefox_driver.quit()
