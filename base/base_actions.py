from selenium.webdriver.common.by import By
from base.logger import customLogger
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from traceback import print_stack


class BaseActions:
    """
        This class contains actions that will be activated in all test cases & all webpages .
    """
    def __init__(self, driver):
        self.driver = driver

    # object of class 'customLogger'
    _log = customLogger()

    def check_element_type(self, locator_type: str):
        """
        This method will check the 'locator_type' of an element and return valid locator type .
        :param locator_type: provided locator type of element .
        :return: valid locator/False .
        """

        # convert 'locator_type' to small case , then check it .
        locator_type_test = locator_type.lower()

        # if the type is valid , then return valid locator .
        if locator_type_test == "id":
            return By.ID
        elif locator_type_test == "name":
            return By.NAME
        elif locator_type_test == "xpath":
            return By.XPATH
        elif locator_type_test == "css":
            return By.CSS_SELECTOR
        elif locator_type_test == "class":
            return By.CLASS_NAME
        elif locator_type_test == "link":
            return By.LINK_TEXT

        # else - show this message .
        else:
            self._log.error(f"MESSAGE FROM - 'check_element_type' - 'base_actions' : "
                            f"LOCATOR TYPE : '{locator_type}' NOT CORRECT/SUPPORTED .")

        return False

    def get_element(self, locator_type: str, locator: str):
        """
        This method overrides the functionality of selenium 'find_element' method .
        the method using 'check_element_type' method from this file -> gets valid type of the element / False .

        :param locator_type: type of the element .
        :param locator: locator of element (xpath, css, id ...)
        :return: Element .
        """
        # check elements type
        locator_type_checked = self.check_element_type(locator_type)

        # if returned 'false' -> invalid locator -> do nothing
        if not locator_type_checked:
            self._log.error(f"MESSAGE FROM - 'get_element' - 'base_actions' : "
                            f"ELEMENT WITH LOCATOR : '{locator}' COULD NOT BE FOUND .")
            return None

        # element is found -> then find the element using 'locator_type_checked' from above and update the log
        try:
            element = self.driver.find_element(locator_type_checked, locator)
            self._log.info(f"MESSAGE FROM - 'get_element' - 'base_actions' : "
                           f"Element with locator : '{locator}' - has been found !")
            return element
        except:
            self._log.error(f"MESSAGE FROM - 'get_element' - 'base_actions' : "
                            f"ELEMENT WITH LOCATOR : '{locator}' COULD NOT BE FOUND .")
            return None

    def get_elements(self, locator_type: str, locator: str):
        """
        This method overrides the functionality of selenium 'find_elements' method .
        the method using 'check_element_type' method from this file -> gets valid type of the element / False .

        :param locator_type: type of elements .
        :param locator: locator of elements (xpath, css, id ...)
        :return: Element .
        """
        if not self.check_element_type(locator_type):
            self._log.error(f"MESSAGE FROM - 'get_elements' - 'base_actions' : "
                            f"ELEMENT WITH LOCATOR : '{locator}' COULD NOT BE FOUND .")
            return None
        else:
            locator_type_checked = self.check_element_type(locator_type)

        try:
            element = self.driver.find_elements(locator_type_checked, locator)
            self._log.info(f"MESSAGE FROM - 'get_elements' - 'base_actions' : "
                           f"{len(element)} Elements with locator : '{locator}' - has been found !")
            return element
        except:
            self._log.error(f"ELEMENT WITH LOCATOR : '{locator}' COULD NOT BE FOUND .")
            return None

    def enter_key_to_field(self, locator_type: str, locator: str, key):
        """
        This method does :
        1. finds the elements using - 'get_element' from this module .
        2. send key to the element using - selenium 'send_keys' .
        3. update log .

        :param locator_type: locator type of an element (id , xpath , css ...)
        :param locator: the locator iself       (for exaple : //[@id='my id'])
        :param key: key that will be sent to the element

        :return: None
        """
        element = self.get_element(locator_type, locator)
        element.send_keys(key)
        self._log.info(f"MESSAGE FROM - 'enter_key_to_field' - 'base_actions' :"
                       f"Sent key to element with locator : '{locator}' .")

    def enter_key_to_fields(self, locator_type: str, locator: str, keys: list):
        """
        This method does :
        1. finds the elements using - 'get_elements' from this module .
        2. send key to the element using - selenium 'send_keys' .
        3. update log .

        :param locator_type: locator type of an element (id , xpath , css ...)
        :param locator: the locator iself       (for exaple : //[@id='my id'])
        :param key: key that will be sent to the element

        :return: None
        """
        elements = self.get_elements(locator_type, locator)

        if len(keys) != len(elements):
            self._log.error("MESSAGE FROM - 'enter_key_to_fields' - 'base_actions' "
                            "ERROR - KEYS & ELEMENTS DONT HAVE SAME LENGTH")
            return None

        for i in range(0, len(elements)):
            elements[i].send_keys(keys[i])

    def click_element(self, locator_type: str = "", locator: str = "", element=None):
        """
        This method does :
        1. finds the element using - 'get_element' from this module .
        2. click the element using - selenium 'click' .
        3. update log .

        :param element:
        :param locator_type: locator type of an element (id , xpath , css ...)
        :param locator: the locator iself       (for exaple : //[@id='my id'])

        :return: None
        """
        if locator_type != "" and locator != "":
            element = self.get_element(locator_type, locator)

        self._log.info(f"MESSAGE FROM - 'click_element' - 'base_actions' :"
                       f"Element with locator : '{locator}' - has been found & and clicked .")
        element.click()

    def click_elements(self, elements=None, locator_type: str = "", locator: str = ""):

        if locator_type != "" and locator != "":
            elements = self.get_elements(locator_type, locator)

        for elem in elements:
            elem.click()
            self._log.info(f"MESSAGE FROM - 'click_element' - 'base_actions' :"
                           f"Element with locator '{locator} - has been clicked .'")

    def is_element_present(self, locator_type: str, locator: str):
        """
        This method checks if element is present in the dom .

        :param driver:
        :param locator_type: ocator type of an element (id , xpath , css ...)
        :param locator: the locator iself       (for exaple : //[@id='my id'])

        :return: True / False
        """
        element = self.get_element(locator_type, locator)

        if element is None:
            self._log.error(f"MESSAGE FROM - 'is_element_present' - 'base_actions' - ELEMENT IS NOT PRESENT .")
            return False

        self._log.info(f"MESSAGE FROM - 'is_element_present' - 'base_actions' - ELEMENT IS PRESENT - RETURN ELEMENT .")
        return element

    def take_screenshot(self):
        """
            Takes screenshot of the current open web page
            :param driver
            :return:
        """
        fileName = str(round(time.time() * 1000)) + ".png"
        screenshotDirectory = "C:\\Users\\vadim\\PycharmProjects\\swagLabsFinal\\screenshots\\"
        destinationFile = screenshotDirectory + fileName  # destination + file name

        try:
            self.driver.save_screenshot(destinationFile)
            print("Screenshot saved to directory --> :: " + destinationFile)
        except NotADirectoryError:
            print("Not a directory issue")

    def wait_for_element(self, locator_type, locator):
        """
        explicit wait for specific element .
        :param locator_type: locator type of element .
        :param locator: locator of element .
        :return:
        """
        element = None
        try:
            locator_type_checked = self.check_element_type(locator_type)
            self._log.info("Waiting for maximum :: 3 :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, 3, poll_frequency=1, ignored_exceptions=[NoSuchElementException,
                                                                                       ElementNotVisibleException,
                                                                                       ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((locator_type_checked, locator)))
            self._log.info(f"MESSAGE FROM - 'wait_for_element' - 'base_actions' : "
                           f"Element with locators : {locator_type_checked} - {locator} - appeared on the web page")
        except:
            self._log.info("MESSAGE FROM - 'wait_for_element' - 'base_actions' : "
                           "Element with locators : {locator_type_checked} - {locator} -  NOT APPEARED ON THE WEB PAGE")
            print_stack()

        return element

    def check_webpage(self, current_webpage, valid_webpage, test_name):
        """
        This method will check if 'current_webpage' if the 'valid_webpage' .
        :param current_webpage: current webpage .
        :param valid_webpage: webpage driver should be on .
        :param test_name: name of the test where this method activated .
        :return:
        """
        # check current page
        if current_webpage != valid_webpage:
            self._log.error(f"### MESSAGE FROM - 'check_webpage' - 'base_actions' : "
                            f"TEST - {test_name} - REACHED TO : {current_webpage} - SUPPOSED TO REACH :"
                            f"{valid_webpage}")
            return False

        # valid
        self._log.info("MESSAGE FROM - 'check_webpage' - 'base_actions' : "
                       f"reached to {valid_webpage} - valid")
        return True

    def check_count_elements(self, elements, amount: int, test_name: str):
        """
        This method will count the 'elements' provided as parameter .

        :param elements: elements provided .
        :param amount: amount of elements should appear .
        :param test_name: name of the test where this method activated .
        :return:
        """
        # check amount of elements
        if len(elements) != amount:
            self._log.error(f"### MESSAGE FROM - 'check_count_elements' - 'base_actions' : "
                            f"TEST - {test_name} - HAS {len(elements)} ITEMS - SUPPOSED TO BE - {amount} .")
            return False

        # valid
        self._log.info(f"MESSAGE FROM - 'check_count_elements' - 'base_actions' : "
                       f"Found {len(elements)} items - supposed to be {amount}")
        return True
