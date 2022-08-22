from base.web_driver_factory import WebDriverFactory
from page.login_page import LoginPage
import unittest
from base.logger import customLogger
from ddt import ddt, data, unpack
from base.read_data import getCSVData


@ddt
class LoginTests(unittest.TestCase):

    log = customLogger()
    # using this class to run tests on required browser
    web_driver = WebDriverFactory("firefox")
    BASE_URL = "https://www.saucedemo.com/"

    @classmethod
    def setUpClass(cls):
        cls.log.info("***** RUN SETUP BEFORE ALL 'LOGIN' TESTS *****\n")

    def setUp(self):
        self.log.info("\n##### RUN SETUP BEFORE EVERY TEST #####.\n")

    @data(*getCSVData("C:\\Users\\vadim\\PycharmProjects\\swagLabsFinal\\csv_files\\valid_login_tests.csv"))
    @unpack
    def test_valid_login(self, user_name, password):
        """
        This test , tests valid usernames & valid passwords .
        expected result : let user login .

        :param user_name: valid username .
        :param password: valid password .
        :return:
        """
        self.log.info("--- RUNNING TEST_VALID_LOGIN ---")
        self.log.info(f"### TESTING : username : {user_name} , password : {password}")

        # create new driver and set up the test
        driver = self.web_driver.getWebDriverInstance()
        driver.maximize_window()
        driver.implicitly_wait(3)
        lg = LoginPage(driver)
        driver.get(self.BASE_URL)

        # login using 'user_name' & 'password' , then check if login succeeded (by checking current url webpage)
        lg.login(user_name, password)
        # result - True/False - True if succeeded to login
        result = lg.verify_login_success(user_name, password)

        driver.quit()
        assert result == True

    @data(*getCSVData("C:\\Users\\vadim\\PycharmProjects\\swagLabsFinal\\csv_files\\invalid_login_tests.csv"))
    @unpack
    def test_invalid_login(self, user_name, password):
        """
        This test , tests invalid/missing - username or password .
        expected result : user should not be able to login .

        :param user_name: missing/invalid username (or valid username & invalid/missing password) .
        :param password: missing/invalid password (or invalid/missing username & valid password) .
        :return:
        """
        self.log.info("--- RUNNING TEST_INVALID_LOGIN ---")
        self.log.info(f"### TESTING : username : {user_name} , password : {password}")

        # create new driver and set up the test
        driver = self.web_driver.getWebDriverInstance()
        driver.maximize_window()
        driver.implicitly_wait(3)
        lg = LoginPage(driver)
        driver.get(self.BASE_URL)

        # try login with invalid user info .
        lg.login(user_name, password)
        # check all cases in 'verify_login_fail' and return if test passed
        result = lg.verify_login_fail(user_name, password)

        driver.quit()
        assert result == True

    @data(*getCSVData("C:\\Users\\vadim\\PycharmProjects\\swagLabsFinal\\csv_files\\valid_login_tests.csv"))
    @unpack
    def test_load_webpage(self, user_name, password):
        """
        This test , tests the webpage loading time when login .
        receive valid users data and check if there is any problem with login .
        expected result : login with no longer than 3 sec .

        :param user_name: users 'user_name' .
        :param password: users 'password' .
        :return:
        """
        self.log.info("--- RUNNING TEST_LOAD_WEBPAGE ---")
        self.log.info(f"### TESTING : username : {user_name} , password : {password}")

        # create new driver and set up the test
        driver = self.web_driver.getWebDriverInstance()
        driver.maximize_window()
        driver.implicitly_wait(3)
        lg = LoginPage(driver)
        driver.get(self.BASE_URL)

        result = lg.check_login_time(user_name, password)

        driver.quit()
        assert result == True

    @data(*getCSVData("C:\\Users\\vadim\\PycharmProjects\\swagLabsFinal\\csv_files\\webpages.csv"))
    @unpack
    def test_login_url_link(self, url):
        self.log.info("--- RUNNING TEST_LOGIN_URL_LINK ---")
        self.log.info(f"### TESTING - LINK : {url}")

        # create new driver and set up the test
        driver = self.web_driver.getWebDriverInstance()
        driver.maximize_window()
        driver.implicitly_wait(3)
        lg = LoginPage(driver)
        driver.get(self.BASE_URL)

        result = lg.check_login_using_url(url)

        driver.quit()
        assert result == True

    def tearDown(self):
        self.log.info("\n##### RUN TEARDOWN AFTER EVERY TEST #####.\n")

    @classmethod
    def tearDownClass(cls):
        cls.log.info("***** RUN TEARDOWN AFTER ALL 'LOGIN' TESTS *****\n")
