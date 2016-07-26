from selenium import webdriver
import time
import unittest
import dautil as dl


NAP_SECS = 10


class SeleniumTest(unittest.TestCase):
    def setUp(self):
        self.logger = dl.log_api.conf_logger(__name__)
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_and_click(self, toggle, text):
        xpath = "//a[@data-toggle='{0}' and contains(text(), '{1}')]"
        xpath = xpath.format(toggle, text)
        elem = dl.web.wait_browser(self.browser, xpath)
        elem.click()

    def test_widget(self):
        self.browser.implicitly_wait(NAP_SECS)
        self.browser.get('http://localhost:8888/notebooks/test_widget.ipynb')

        try:
            # Cell menu
            xpath = '//*[@id="menus"]/div/div/ul/li[5]/a'
            link = dl.web.wait_browser(self.browser, xpath)
            link.click()
            time.sleep(1)

            # Run all
            xpath = '//*[@id="run_all_cells"]/a'
            link = dl.web.wait_browser(self.browser, xpath)
            link.click()
            time.sleep(1)

            self.wait_and_click('tab', 'Figure')
            self.wait_and_click('collapse', 'figure.figsize')
        except Exception:
            self.logger.warning('Error while waiting to click', exc_info=True)
            self.browser.quit()

        time.sleep(NAP_SECS)
        self.browser.save_screenshot('widgets_screenshot.png')

if __name__ == "__main__":
    unittest.main()
