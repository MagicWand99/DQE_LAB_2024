from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
import pytest

pytestmark = pytest.mark.integration
driver = webdriver.Chrome()

def test_phptravels_locators():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

driver.get("https://phptravels.com/demo/")

first_name = driver.find_element(By.CLASS_NAME, "first_name")
last_name = driver.find_element(By.CLASS_NAME, "last_name")
business_name = driver.find_element(By.CLASS_NAME, "company_name")
email = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'Access Live Demo')]")
# rRlative locator: find the field positioned directly below "email", locate directly using locate_with
result_field = driver.find_element(locate_with(By.TAG_NAME, "input").below(email))

print("Site 1 elements found:", first_name, last_name, business_name, email, submit_btn)

driver.get("https://phptravels.org/register.php")

reg_first_name = driver.find_element(By.ID, "inputFirstName")
reg_email = driver.find_element(By.NAME, "email")
reg_company = driver.find_element(By.CLASS_NAME, "field")
reg_city = driver.find_element(By.CSS_SELECTOR, "#inputCity")
reg_state = driver.find_element(By.XPATH, "//input[@id='stateinput']")

print("Site 2 elements found:", reg_first_name, reg_email, reg_company, reg_city, reg_state)

driver.get("https://phptravels.com/blog/")

nav_search = driver.find_element(By.CSS_SELECTOR, "svg[class*='h-[18px]']")
first_story_link = driver.find_element(By.XPATH, "(//span[text()='arrow_forward'])[1]")

print("Site 3 elements found:", nav_search, first_story_link)

driver.quit()
