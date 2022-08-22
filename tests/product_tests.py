from base.web_driver_factory import WebDriverFactory
from base.navigation import Navigation
from page.product_page import ProductPage
import unittest
from base.logger import customLogger
from ddt import ddt, data, unpack
from base.read_data import getCSVData


@ddt
class ItemsTests(unittest.TestCase):

    log = customLogger()
    # using this class to run tests on required browser
    web_driver = WebDriverFactory("firefox")
    BASE_URL = "https://www.saucedemo.com/"

    @classmethod
    def setUpClass(cls):
        cls.log.info("***** RUN SETUP BEFORE ALL 'ITEMS' TESTS *****\n")

    def setUp(self):
        self.log.info("\n##### RUN SETUP BEFORE EVERY TEST #####.\n")

    def test_count_items(self):
        """
        This test check how many items appear on 'product' page .
        1. log in to website using 'navigator' of 'Navigation' module from 'base' package .
        2. count items appear on 'product' page - using 'count_items' of 'ProductPage' module .
        :return:
        """
        self.log.info("--- RUNNING TEST_COUNT_ITEMS ---")

        # create new driver and set up the test
        driver = self.web_driver.getWebDriverInstance()
        driver.maximize_window()
        driver.implicitly_wait(3)
        navigator = Navigation(driver)
        pp = ProductPage(driver)
        driver.get(self.BASE_URL)

        # login to page then count the items appear on 'items page'
        navigator.navigate_to_product_page()
        result = pp.count_items()

        driver.quit()
        assert result == True

    def test_add_remove_buttons(self):
        """
        This test , tests the functionality of 'add to cart' & 'remove' buttons on items appear on 'product' page .
        1. navigate to 'product' page - using 'navigate_to_product_page' of 'Navigation' module .
        2. test functionality - using 'add_remove_items' of 'ProductPage' module .
        :return:
        """
        self.log.info("--- RUNNING TEST_ADD_REMOVE_BUTTONS ---")

        # create new driver and set up the test
        driver = self.web_driver.getWebDriverInstance()
        driver.maximize_window()
        driver.implicitly_wait(3)
        navigator = Navigation(driver)
        pp = ProductPage(driver)
        driver.get(self.BASE_URL)

        # navigate to 'product' page
        navigator.navigate_to_product_page()
        # test buttons - using 'add_remove_items' of 'ProductPage' module
        result = pp.add_remove_items()

        driver.quit()
        assert result == True

    @data(*getCSVData("C:\\Users\\vadim\\PycharmProjects\\swagLabsFinal\\csv_files\\sort_options.csv"))
    @unpack
    def test_sorting_element(self, option):
        """
        This method tests the sorting functionality .
        test will log in , then click on each sorting option , then check if the items appear in chosen option .
        1. navigate to 'product' page - using 'navigate_to_product_page' of 'Navigation' module .
        2. test sorting element - using 'sort_options' & 'check_sort_option' of 'ProductPage' module .

        :param option: order option
        :return:
        """
        # create new driver and set up the test
        driver = self.web_driver.getWebDriverInstance()
        driver.maximize_window()
        driver.implicitly_wait(3)
        driver.get(self.BASE_URL)
        navigator = Navigation(driver)
        pp = ProductPage(driver)

        # there is 4 options to sort the items in the website
        if int(option) == 1:
            self.log.info("--- RUNNING TEST_SORT - A TO Z ---\n")
        elif int(option) == 2:
            self.log.info("--- RUNNING TEST_SORT - Z TO A ---\n")
        elif int(option) == 3:
            self.log.info("--- RUNNING TEST_SORT - PRICE - LOW TO HIGH ---\n")
        elif int(option) == 4:
            self.log.info("--- RUNNING TEST_SORT - PRICE - HIGH TO LOW ---\n")

        # navigate to 'product' page
        navigator.navigate_to_product_page()
        # use 'sort_options' & 'check_sort_option' from 'ProductPage' module to check functionality of sorting element
        pp.sort_options(option)
        result = pp.check_sort_option(option)

        driver.quit()
        assert result == True

    def tearDown(self):
        self.log.info("\n##### RUN TEARDOWN AFTER EVERY TEST #####.\n")

    @classmethod
    def tearDownClass(cls):
        cls.log.info("***** RUN TEARDOWN AFTER ALL 'ITEMS' TESTS *****\n")

