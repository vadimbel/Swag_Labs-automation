from base.base_actions import BaseActions
from base.logger import customLogger


class YourInfoPage(BaseActions):
    """
        This module contains functions that will be used on 'your info' page .
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # object of class 'customLogger' - to be able to write into the log when using function from this module
    log = customLogger()

    OVERVIEW_PAGE_URL = "https://www.saucedemo.com/checkout-step-two.html"

    # types
    first_name_type = "id"
    last_name_type = "id"
    code_type = "id"
    continue_button_type = "id"
    error_message_type = "xpath"

    # locators
    first_name_locator = "first-name"
    last_name_locator = "last-name"
    code_locator = "postal-code"
    continue_button_locator = "continue"
    error_message_locator = "//h3[@data-test='error']"

    def enter_info_to_fields(self, first_name, last_name, code):
        """
        This method will be activated in 'test_valid_user_info' from 'your_info_tests' file .
        finds all 3 text fields on 'information' page , and enter text to them .
        :param first_name: key for 'first name' field .
        :param last_name: key for 'last name' field .
        :param code: key for 'code/postal' field .
        :return:
        """
        # enter user info to text fields
        self.enter_key_to_field(self.first_name_type, self.first_name_locator, first_name)
        self.enter_key_to_field(self.last_name_type, self.last_name_locator, last_name)
        self.enter_key_to_field(self.code_type, self.code_locator, code)

    def verify_valid_user_info(self, first_name, last_name, code):
        """
        This method will be activated in 'test_valid_user_info' from 'your_info_tests' file .
        After enter user info - using 'enter_info_to_fields' from this module , this method click 'continue' button
        then check if webpage moved to 'overview' page .

        :return:
        """
        test_name = "TEST_VALID_USER_INFO"

        # click 'continue' button
        self.click_element(self.continue_button_type, self.continue_button_locator)

        # check if moved to 'overview' page
        if not self.check_webpage(self.driver.current_url, self.OVERVIEW_PAGE_URL, test_name):
            self.test_fail_message(test_name, 2, f"### TEST INFO : {first_name} , {last_name} , {code}")
            return False

        self.test_pass_message(test_name, 2, f"### TEST INFO : {first_name} , {last_name} , {code}")
        return True

    def verify_invalid_user_info(self, first_name, last_name, code):
        """
        This method will be activated on 'test_invalid_user_info' from 'your_info_tests' file .
        check if the right error message appear when fill 3 text fields on 'information' page incorrectly .
        :param first_name: key for 'first_name' text filed .
        :param last_name: key for 'last_name' text filed .
        :param code: key for 'code/postal' text field .
        :return:
        """
        test_name = "TEST_INVALID_USER_INFO"

        # all error messages for this page :
        FIRST_NAME_MESSAGE = "Error: First Name is required"
        LAST_NAME_MESSAGE = "Error: Last Name is required"
        CODE_MESSAGE = "Error: Postal Code is required"

        message_element = None

        # click on 'continue' button
        self.click_element(self.continue_button_type, self.continue_button_locator)

        # if 'first_name' is missing -> 'FIRST_NAME_MESSAGE' should appear
        if first_name == "":
            self.log.info(f"### FIRST NAME - IS MISSING")
            # check if right message appear
            message_element = self.get_element(self.error_message_type, self.error_message_locator)
            if message_element.text != FIRST_NAME_MESSAGE:
                self.log.error(f"TEST - {test_name} - MESSAGE APPEARED : {message_element.text}"
                               f" - SHOULD BE : {FIRST_NAME_MESSAGE}")
                self.test_fail_message(test_name)
                return False

        # elif 'last_name' is missing -> 'LAST_NAME_MESSAGE' should appear
        elif last_name == "":
            self.log.info(f"### LAST NAME - IS MISSING")
            # check if right message appear
            message_element = self.get_element(self.error_message_type, self.error_message_locator)
            if message_element.text != LAST_NAME_MESSAGE:
                self.log.error(f"TEST - {test_name} - MESSAGE APPEARED : {message_element.text}"
                               f" - SHOULD BE : {LAST_NAME_MESSAGE}")
                self.test_fail_message(test_name)
                return False

        # elif 'postal/code' is missing -> 'CODE_MESSAGE' should appear
        elif code == "":
            self.log.info(f"### CODE - IS MISSING")
            # check if right message appear
            message_element = self.get_element(self.error_message_type, self.error_message_locator)
            if message_element.text != CODE_MESSAGE:
                self.log.error(f"TEST - {test_name} - MESSAGE APPEARED : {message_element.text}"
                               f" - SHOULD BE : {CODE_MESSAGE}")
                self.test_fail_message(test_name)
                return False

        # if all fields are not empty , test passed
        self.log.info(f"ERROR MESSAGE IS : {message_element.text}")
        self.test_pass_message(test_name)
        return True

    def test_pass_message(self, test_name: str, option: int = 1, info: str = ""):
        if option == 1:
            self.log.info(f"### TEST - {test_name} - PASSED")
        elif option == 2:
            self.log.info(f"### TEST - {test_name} - {info} - PASSED")
        else:
            self.log.error("### INVALID 'test_pass_message' - 'your_info_page' - OPTION .")

    def test_fail_message(self, test_name, option: int = 1, info: str = ""):
        self.take_screenshot()
        if option == 1:
            self.log.error(f"### TEST - {test_name} - VALID")
        elif option == 2:
            self.log.info(f"### TEST - {test_name} - {info} - PASSED")
        else:
            self.log.error("### INVALID FROM - 'test_fail_message' - 'your_info_page' - OPTION .")

