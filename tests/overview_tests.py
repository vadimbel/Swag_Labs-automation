from base.web_driver_factory import WebDriverFactory
from page.overview_page import OverviewPage
from base.navigation import Navigation
import unittest
from base.logger import customLogger
from ddt import ddt, data, unpack
from base.read_data import getCSVData


@ddt
class OverviewTests(unittest.TestCase):
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

    @data(*getCSVData("C:\\Users\\vadim\\PycharmProjects\\swagLabsFinal\\csv_files\\values.csv"))
    @unpack
    def test_total_sum(self, amount):
        """
        This test :
        1. on 'product' page -> find first 'amount' 'add to cart' buttons and click them -> add 'amount' items to cart
        and save the prices of the item were added .
        2. move to 'overview' page and check if the prices displayed are valid .

        :param amount: amount of items to add on 'product' page .
        :return:
        """
        self.log.info("--- RUNNING TEST_TOTAL_SUM---")

        # create new driver and set up the test
        driver = self.web_driver.getWebDriverInstance()
        driver.maximize_window()
        driver.implicitly_wait(3)
        op = OverviewPage(driver)
        navigator = Navigation(driver)

        # navigate to 'product' page
        navigator.navigate_to_product_page()

        # on 'product' page -> add 'amount' items & get all prices and save them in a variable
        total_sum = op.add_items(int(amount))

        # move to 'overview' page and check if 'item total' equals to 'total_sum' from above
        # then get 'Tax' from 'overview' page and check if 'item total' + 'Tax' == 'Total'
        navigator.navigate_to_overview_page_from_product_page()
        result = op.check_item_total(total_sum)

        driver.quit()
        assert result == True

    def tearDown(self):
        self.log.info("\n##### RUN TEARDOWN AFTER EVERY TEST #####.\n")

    @classmethod
    def tearDownClass(cls):
        cls.log.info("***** RUN TEARDOWN AFTER ALL 'YOUR_INFO' TESTS *****\n")
