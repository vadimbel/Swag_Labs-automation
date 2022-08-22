import time
from base.base_actions import BaseActions
from base.logger import customLogger


class LoginPage(BaseActions):
    """
    This module contains functions that will be used on 'login' page .
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    BASE_URL = "https://www.saucedemo.com/"
    MAIN_PAGE_URL = "https://www.saucedemo.com/inventory.html"

    # object of class 'customLogger' - to be able to write into the log when using function from this module
    _log = customLogger()

    # locators_type - of elements be used on 'login' page
    user_name_type = "id"
    password_type = "id"
    login_button_type = "id"
    error_login_message_type = "xpath"
    shopping_cart_type = "class"

    # locators - of elements will be used
    user_name_locator = "user-name"
    password_locator = "password"
    login_button_locator = "login-button"
    error_login_message_locator = '//h3[@data-test="error"]'
    shopping_cart_locator = "shopping_cart_link"

    # error messages
    case_one = "Epic sadface: Password is required"     # not empty user_name & empty password
    case_two = "Epic sadface: Username is required"     # empty user_name & not empty password
    case_three = "Epic sadface: Username and password do not match any user in this service" # invalid username & password
    case_four = "Epic sadface: Sorry, this user has been locked out."       # login with locked user info

    # info of locked out users - get this info from sql
    locked_out_users = {
        "locked_out_user": "secret_sauce",
    }

    def login(self, user_name, password):
        """
        This method will be activated in many tests -> login to website .
        :param user_name: username tested .
        :param password: password tested .
        :return:
        """
        # find 'user_name' element and send key to field
        self.enter_key_to_field(self.user_name_type, self.user_name_locator, user_name)

        # find 'password' element and send key to field
        self.enter_key_to_field(self.password_type, self.password_locator, password)

        # find 'login' element and click it
        self.click_element(self.login_button_type, self.login_button_locator)

    def verify_login_success(self, user_name, password):
        """
        This method check if user was able to login with provided valid 'user_name' & 'password' .
        :param user_name: username tested .
        :param password: password tested .
        :return:
        """
        # check if reached the main_page webpage
        if not self.check_webpage(self.driver.current_url, self.MAIN_PAGE_URL, "TEST_VALID_LOGIN"):
            self.test_fail_message(user_name, password)
            return False

        self.test_pass_message(user_name, password)
        return True

    def verify_login_fail(self, user_name, password):
        """
        This method check if user was able to log in with invalid/missing 'user_name' or 'password' .
        :param user_name: username tested .
        :param password: password tested .
        :return:
        """
        # check if able login with invalid user info (by checking the webpage)
        if not self.check_webpage(self.driver.current_url, self.BASE_URL, "TEST_INVALID_LOGIN"):
            self.test_fail_message(user_name, password)
            return False

        # error message should pop up when try login with invalid user info - try find it
        element = self.is_element_present(self.error_login_message_type, self.error_login_message_locator)
        # if not found -> test failed
        if not element:
            self.test_fail_message(user_name, password)
            return False

        # special case : locked out user info .
        if user_name in self.locked_out_users and self.locked_out_users[user_name] == password:
            if element.text != self.case_four:
                self._log.error(f"### message is - {element.text} - supposed to be {self.case_four} - INVALID")
                self.test_fail_message(user_name, password)
                return False
            # update log that a valid message appeared
            self._log.info(f"### message is - {element.text} - valid")

        # case 1 - not empty valid/invalid username & empty password (not entered)
        # text in this case should be : "Epic sadface: Password is required"
        elif user_name != "" and password == "":
            if element.text != self.case_one:
                self._log.error(f"### message is - {element.text} - supposed to be {self.case_one} - INVALID")
                self.test_fail_message(user_name, password)
                return False
            # update log that a valid message appeared
            self._log.info(f"### message is - {element.text} - valid")

        # case 2 - empty username (not entered) & not empty valid/invalid password
        # text in this case should be : "Epic sadface: Username is required"
        elif user_name == "" and password != "":
            if element.text != self.case_two:
                self._log.error(f"### message is - {element.text} - supposed to be {self.case_two} - INVALID")
                self.test_fail_message(user_name, password)
                return False
            # update log that a valid message appeared
            self._log.info(f"### message is - {element.text} - valid")

        # case 3 - empty username & password
        # text in this case should be : "Epic sadface: Username is required"
        elif user_name == "" and password == "":
            if element.text != self.case_two:
                self._log.error(f"### message is - {element.text} - supposed to be {self.case_two} - INVALID")
                self.test_fail_message(user_name, password)
                return False
            # update log that a valid message appeared
            self._log.info(f"### message is - {element.text} - valid")

        # case 4 - not empty , invalid username or password
        # text in this case should be : "Epic sadface: Username is required"
        else:
            if element.text != self.case_three:
                self._log.error(f"### message is - {element.text} - supposed to be {self.case_three} - INVALID")
                self.test_fail_message(user_name, password)
                return False
            # update log that a valid message appeared
            self._log.info(f"### message is - {element.text} - valid")

        # passed all invalid cases -> test passed
        self.test_pass_message(user_name, password)
        return True

    def check_login_time(self, user_name, password):
        """
        This method checks the time it takes to log in with provided 'user_name' & 'password' .
        :param user_name: username tested .
        :param password: password tested .
        :return:
        """
        self.login(user_name, password)
        start = time.time()

        # find 'cart' element on 'product' webpage
        cart_element = self.wait_for_element(self.shopping_cart_type, self.shopping_cart_locator)
        if not cart_element:
            self._log.error(f"### TEST - element with {self.shopping_cart_type} , {self.shopping_cart_locator} did not"
                            f" found")
            self.test_fail_message(user_name, password)
            return False

        end = time.time()

        # took more than 3 sec -> fail
        if end - start > 3:
            self._log.error(f"### TEST - login with values : {user_name} , {password} - TOOK MORE THEN 3 SEC .")
            self.test_fail_message(user_name, password)
            return False

        # able login with less than 3 sec -> pass
        self._log.info(f"### logged in with values : {user_name} , {password} - with {end-start} sec - valid .")
        self.test_pass_message(user_name, password)
        return True

    def check_login_using_url(self, url):
        """
        This method check if user can enter pages in the website using url link without login to the website .
        expected result : user should not be able to move to 'url' page .

        :param url: url link to webpage in the website .
        :return:
        """
        self.driver.get(url)
        result = self.check_webpage(self.driver.current_url, self.BASE_URL, "TEST_LOGIN_URL_LINK")

        if not result:
            self._log.error(f"### TEST - TEST_LOGIN_URL_LINK - WAS ABLE TO LOGIN USING URL LINK - FAIL .\n")
            return False

        self._log.info(f"### TEST - TEST_LOGIN_URL_LINK - pass .")
        return True

    def test_pass_message(self, user_name, password):
        self._log.info(f"### TEST : username : '{user_name}' , password : '{password}' - PASS .\n")

    def test_fail_message(self, user_name, password):
        self.take_screenshot()
        self._log.error(f"### TEST : username : '{user_name}' , password : '{password}' - FAIL .\n")
