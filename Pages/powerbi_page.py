from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class PowerBIPage:
    URL = "https://playground.powerbi.com/en-us/showcases-gallery/capture-report-views"

    REPORT_IFRAME = (By.TAG_NAME, "iframe")                     # verify in DevTools
    SAVED_VIEWS_BUTTON = (By.XPATH, "//button[contains(., 'Saved views')]")
    CAPTURE_VIEW_BUTTON = (By.XPATH, "//button[contains(., 'Capture view')]")

    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(self.URL)

    def switch_to_report(self):
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.REPORT_IFRAME))

    def is_saved_views_button_displayed(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.SAVED_VIEWS_BUTTON)
        ).is_displayed()

    def is_capture_view_button_displayed(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.CAPTURE_VIEW_BUTTON)
        ).is_displayed()
    
    def open_page(self):
        self.driver.get(self.URL)