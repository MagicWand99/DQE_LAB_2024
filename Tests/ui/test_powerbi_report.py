import pytest
from pages.powerbi_page import PowerBIPage

pytestmark = pytest.mark.ui

@pytest.fixture
def powerbi_page(driver):
    page = PowerBIPage(driver)
    page.open_page()
    page.switch_to_report()
    return page

@pytest.mark.ui
class TestPowerBIReport:
    def test_saved_views_button_is_displayed(self, powerbi_page):
        assert powerbi_page.is_saved_views_button_displayed(), \
            "'Saved views' button should be visible in the report"

    def test_capture_view_button_is_displayed(self, powerbi_page):
        assert powerbi_page.is_capture_view_button_displayed(), \
            "'Capture view' button should be visible in the report"
