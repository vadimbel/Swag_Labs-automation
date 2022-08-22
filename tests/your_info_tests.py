from base.web_driver_factory import WebDriverFactory
from page.your_info_page import YourInfoPage
from base.navigation import Navigation
import unittest
from base.logger import customLogger
from ddt import ddt, data, unpack
from base.read_data import getCSVData


@ddt
class YourInfoTests(unittest.TestCase):

    log = customLogger()
    web_driver = WebDriverFactory("firefox")
    BASE_URL = "https://www.saucedemo.com/"

    VALID_USER_NAME = "standard_user"
    VALID_PASSWORD = "secret_sauce"

    @classmethod
    def setUpClass(cls):
        cls.log.info("***** RUN SETUP BEFORE ALL 'YOUR_INFO' TESTS *****\n")

    def setUp(self):
        self.log.info("\n##### RUN SETUP BEFORE EVERY TEST #####.\n")

    @data(*getCSVData("C:\\Users\\vadim\\PycharmProjects\\swagLabsFinal\\csv_files\\user_info.csv"))
    @unpack
    def test_valid_user_info(self, first_name, last_name, code):
        """
        This test , tests the functionality of 'continue' button on 'information' page .
        :param first_name: first name entered to 'first name' text field on 'information' page .
        :param last_name: last name entered to 'last name' text field on 'information' page .
        :param code: code/postal entered to 'code/postal' text field on 'information' page .
        :return:
        """
        self.log.info("--- RUNNING TEST_VALID_USER_INFO ---")
        self.log.info(f"### TESTING - {first_name} , {last_name} , {code}")

        # create new driver and set up the test
        driver = self.web_driver.getWebDriverInstance()
        driver.maximize_window()
        driver.implicitly_wait(3)
        yip = YourInfoPage(driver)
        navigator = Navigation(driver)

        # navigate to 'product' page
        navigator.navigate_to_product_page()

        # navigate to 'your cart' page
        navigator.navigate_to_your_cart_page()

        # navigate to 'your information' page
        navigator.navigate_to_your_information_page()

        # enter info to fields
        yip.enter_info_to_fields(first_name, last_name, code)

        # click on 'continue' and check if reached to next page
        result = yip.verify_valid_user_info(first_name, last_name, code)

        driver.quit()
        assert result == True

    @data(*getCSVData("C:\\Users\\vadim\\PycharmProjects\\swagLabsFinal\\csv_files\\invalid_user_info.csv"))
    @unpack
    def test_invalid_user_info(self, first_name, last_name, code):
        """
        This test tests the error messages that should appear when users did not fill 3 text fields correctly .
        ### one of the parameters (first_name , last_name , code) is not valid (!!)
        :param first_name: key for 'first name' text field .
        :param last_name: key for 'last name' text field .
        :param code: key for 'code/postal' text field .
        :return:
        """
        self.log.info("--- RUNNING TEST_INVALID_USER_INFO ---")
        self.log.info(f"### TESTING - {first_name} , {last_name} , {code}")

        # create new driver and set up the test
        driver = self.web_driver.getWebDriverInstance()
        driver.maximize_window()
        driver.implicitly_wait(3)
        yip = YourInfoPage(driver)
        navigator = Navigation(driver)

        # navigate to 'product' page
        navigator.navigate_to_product_page()

        # navigate to 'your cart' page
        navigator.navigate_to_your_cart_page()

        # navigate to 'your information' page
        navigator.navigate_to_your_information_page()

        # enter info to fields
        yip.enter_info_to_fields(first_name, last_name, code)

        # check the error message appear
        result = yip.verify_invalid_user_info(first_name, last_name, code)

        driver.quit()
        assert result == True

    def tearDown(self):
        self.log.info("\n##### RUN TEARDOWN AFTER EVERY TEST #####.\n")

    @classmethod
    def tearDownClass(cls):
        cls.log.info("***** RUN TEARDOWN AFTER ALL 'YOUR_INFO' TESTS *****\n")
