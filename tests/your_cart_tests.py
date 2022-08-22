from base.web_driver_factory import WebDriverFactory
from page.your_cart_page import YourCartPage
from base.navigation import Navigation
import unittest
from base.logger import customLogger
from ddt import ddt, data, unpack
from base.read_data import getCSVData


@ddt
class YourCartTests(unittest.TestCase):

    log = customLogger()
    # using this class to run tests on required browser
    web_driver = WebDriverFactory("firefox")
    BASE_URL = "https://www.saucedemo.com/"

    VALID_USER_NAME = "standard_user"
    VALID_PASSWORD = "secret_sauce"

    @classmethod
    def setUpClass(cls):
        cls.log.info("***** RUN SETUP BEFORE ALL 'YOUR_CART' TESTS *****\n")

    def setUp(self):
        self.log.info("\n##### RUN SETUP BEFORE EVERY TEST #####.\n")

    def test_continue_shopping_button(self):
        """
        This test , tests the functionality of 'continue shopping' button on 'your cart' webpage .
        expected result : click on 'continue shopping' -> move to 'product' page .
        :return:
        """
        self.log.info("--- RUNNING TEST_CONTINUE_SHOPPING_BUTTON ---")

        # create new driver and set up the test
        driver = self.web_driver.getWebDriverInstance()
        driver.maximize_window()
        driver.implicitly_wait(3)
        ycp = YourCartPage(driver)
        navigator = Navigation(driver)

        # navigate to 'your cart' page
        navigator.navigate_to_product_page()
        navigator.navigate_to_your_cart_page()

        # check button
        result = ycp.check_continue_shopping_button()

        driver.quit()
        assert result == True

    def test_checkout_button(self):
        """
        This test , tests the functionality of 'checkout' button on 'your cart' webpage .
        expected result : click on 'checkout' -> move to 'information' page .
        :return:
        """
        self.log.info("--- RUNNING TEST_CHECKOUT_BUTTON ---")

        # create new driver and set up the test
        driver = self.web_driver.getWebDriverInstance()
        driver.maximize_window()
        driver.implicitly_wait(3)
        ycp = YourCartPage(driver)
        navigator = Navigation(driver)

        # navigate to 'your cart' page
        navigator.navigate_to_product_page()
        navigator.navigate_to_your_cart_page()

        # check button
        result = ycp.check_checkout_button()

        driver.quit()
        assert result == True

    @data(*getCSVData("C:\\Users\\vadim\\PycharmProjects\\swagLabsFinal\\csv_files\\item_locators.csv"))
    @unpack
    def test_click_on_item(self, item_type, item_locator, item):
        """
        In this test :
        1. navigate to 'product' page and add item to cart .
        2. navigate to 'your cart' page .
        3. click on the item added to cart from 'your cart' page .
        4. then check if the webpage appeared is the page of the elements was added on 'your cart' page .

        :param item_type: type of element locator
        :param item_locator: locator of element
        :param item: number of element
        :return:
        """
        self.log.info("--- RUNNING TEST_CLICK_ON_ITEM ---")

        # create new driver and set up the test
        driver = self.web_driver.getWebDriverInstance()
        driver.maximize_window()
        driver.implicitly_wait(3)
        ycp = YourCartPage(driver)
        navigator = Navigation(driver)

        # navigate to 'product' page
        navigator.navigate_to_product_page()

        # on 'product' page - add new item to cart
        ycp.add_item(item_type, item_locator, item)

        # navigate to 'your cart' page
        navigator.navigate_to_your_cart_page()

        # on 'your cart' page - click on element text and check if the right webpage opened
        result = ycp.click_item()

        driver.quit()
        assert result == True

    @data(*getCSVData("C:\\Users\\vadim\\PycharmProjects\\swagLabsFinal\\csv_files\\item_locators.csv"))
    @unpack
    def test_remove_button(self, locator_type, locator, item):
        """
        This test tests the functionality if 'remove' button on the webpage appeared after clicking items text of an
        item was added to cart on 'product' page .

        :param locator_type:
        :param locator:
        :param item:
        :return:
        """
        self.log.info("--- RUNNING TEST_REMOVE_BUTTON ---")

        # create new driver and set up the test
        driver = self.web_driver.getWebDriverInstance()
        driver.maximize_window()
        driver.implicitly_wait(3)
        ycp = YourCartPage(driver)
        navigator = Navigation(driver)

        # navigate to 'product' page
        navigator.navigate_to_product_page()

        # on 'product' page - add new element to cart
        ycp.add_item(locator_type, locator, item)

        # navigate to 'your cart' page
        navigator.navigate_to_your_cart_page()

        # from 'your cart' page - remove added item from cart , and check if item removed
        result = ycp.remove_item()

        driver.quit()
        assert result == True

    def tearDown(self):
        self.log.info("\n##### RUN TEARDOWN AFTER EVERY TEST #####.\n")

    @classmethod
    def tearDownClass(cls):
        cls.log.info("***** RUN TEARDOWN AFTER ALL 'YOUR_CART' TESTS *****\n")
