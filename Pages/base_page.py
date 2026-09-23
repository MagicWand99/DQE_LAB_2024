from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class BasePage:
    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)

    def find_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def is_displayed(self, locator):
        return self.find_visible(locator).is_displayed()

    def switch_to_frame(self, locator):
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(locator))

    def switch_to_default(self):
        self.driver.switch_to.default_content()
