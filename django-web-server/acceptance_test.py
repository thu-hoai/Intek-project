import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class ConnectionTest(unittest.TestCase):
    def setUp(self):
        """Run before each test"""
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def tearDown(self):
        """Run after each test to stop our browse"""
        self.browser.quit()

    def test_connection_page_works(self):
        """User story Connection page"""
        # Get the home page
        self.browser.get('http://localhost:8000')
        # Test for the first page Connection
        self.assertIn('Connection', self.browser.title)
        # header_text = self.browser.find_element_by_tag_name('h1').text

        # Input username and password
        username = self.browser.find_element_by_class_name('main_box_form_email_input')
        self.assertEqual(username.get_attribute('placeholder'), 'Username')
        password = self.browser.find_element_by_class_name('main_box_form_password_input')
        self.assertEqual(password.get_attribute('placeholder'), 'Password')

        # username.send_keys('')

if __name__ == "__main__":
    unittest.main(warnings='ignore')
