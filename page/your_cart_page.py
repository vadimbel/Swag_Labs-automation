from base.base_actions import BaseActions
from base.logger import customLogger


class YourCartPage(BaseActions):
    """
    This module contains functions that will be used on 'your info' page .
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    PRODUCT_PAGE_URL = "https://www.saucedemo.com/inventory.html"
    YOUR_INFORMATION_URL = "https://www.saucedemo.com/checkout-step-one.html"

    # object of class 'customLogger' - to be able to write into the log when using function from this module
    log = customLogger()

    # locators type
    continue_shopping_type = "id"
    cart_icon_type = "class"
    item_name_type = "xpath"
    item_name_next_type = "xpath"
    remove_button_type = "xpath"
    cart_item_type = "xpath"
    checkout_button_type = "xpath"

    # locators
    continue_shopping_locator = "continue-shopping"
    cart_icon_locator = "shopping_cart_container"
    item_name_locator = "//div[@class='inventory_item_name']"
    item_name_next_locator = "//div[@class='inventory_details_name large_size']"
    remove_button_locator = '//button[@class="btn btn_secondary btn_small cart_button"]'
    cart_item_locator = '//div[@class="cart_item"]'
    checkout_button_locator = '//button[@id="checkout"]'

    def click_cart_icon(self):
        self.click_element(self.cart_icon_type, self.cart_icon_locator)

    def check_continue_shopping_button(self):
        """
        This method will be used in 'test_continue_shopping_button' test from 'your_cart_tests' .
        This method checks the functionality of 'continue shopping' button from 'YOUR CART' webpage ,
        finds the element and click it , then check if webpage reached to 'product' page .
        :return:
        """
        test_name = "TEST_CONTINUE_SHOPPING_BUTTON"

        # find and click 'continue shopping' button
        self.click_element(self.continue_shopping_type, self.continue_shopping_locator)

        # check if reached to 'product' page
        if not self.check_webpage(self.driver.current_url, self.PRODUCT_PAGE_URL, test_name):
            self.test_fail_message(test_name)
            return False

        self.test_pass_message(test_name)
        return True

    def check_checkout_button(self):
        """
        This method will be used in 'test_checkout_button' test from 'your_cart_tests' .
        This method checks the functionality of 'checkout' button from 'YOUR CART' webpage ,
        :return:
        """
        # name of the test
        test_name = "TEST_CHECKOUT_BUTTON"

        # click on 'checkout' button
        self.click_element(self.checkout_button_type, self.checkout_button_locator)

        # check if reached to 'your information' page
        if not self.check_webpage(self.driver.current_url, self.YOUR_INFORMATION_URL, test_name):
            self.test_fail_message(test_name)
            return False

        self.test_pass_message(test_name)
        return True

    def add_item(self, locator_type, locator, item):
        """
        This method will be activated in "test_click_on_item" test from 'your_cart_tests' .
        On 'product' page , find 'add to cart' button and click it .
        locator_type & locator . 'item' will be used to create valid 'locator' to an item .

        :param locator_type: type of locator .
        :param locator: locator of element .
        :param item: number of element will be added - used to create valid locator .
        :return:
        """
        # create new locator with 'item'
        locator_new = locator.format(item)
        # find 'add to cart' button and click it
        self.click_element(locator_type=locator_type, locator=locator_new)

    def click_item(self):
        """
        This method will be activated in "test_click_on_item" test from 'your_cart_tests' .
        on 'your cart' page , click on the element was added on 'product' page , then check if right webpage was opened.
        :return:
        """
        test_name = "TEST_CLICK_ON_ITEM"

        # locate element on 'your cart' page , save his text , then click it
        item = self.get_element(self.item_name_type, self.item_name_locator)
        item_text = item.text
        self.click_element(element=item)

        # get the text from the page popped out and check if equals to the text saved above
        next_item = self.get_element(self.item_name_next_type, self.item_name_next_locator)

        if next_item.text != item_text:
            self.log.error(f"### TEST - {test_name} - TEXT IS : {next_item.text}"
                           f" - SUPPOSED TO BE : {item_text} - INVALID")
            self.test_fail_message(test_name)
            return False

        self.log.info(f"### TEST - {test_name} - TEXT IS : {next_item.text} - VALID")
        self.test_pass_message(test_name)
        return True

    def remove_item(self):
        """
        This method will be activated in "test_remove_button" test from "your_cart_page" page .
        On 'your cart' page , locate 'remove' button then click it and check if item was removed from cart .
        :return:
        """
        test_name = "TEST_REMOVE_BUTTON"
        # click on remove button
        self.click_element(self.remove_button_type, self.remove_button_locator)

        # check if 'item' removed from cart , element should not be found
        element = self.is_element_present(self.cart_item_type, self.cart_item_locator)
        if not element:
            self.log.info(f"### TEST - {test_name} - ITEM WAS REMOVED - VALID")
            self.test_pass_message(test_name)
            return True

        self.log.info(f"### TEST - {test_name} - ITEM WAS NOT REMOVED ! - INVALID")
        self.test_fail_message(test_name)
        return False

    def test_pass_message(self, test_name):
        self.log.info(f"### TEST - {test_name} - PASS")

    def test_fail_message(self, test_name):
        self.take_screenshot()
        self.log.error(f"### TEST - {test_name} - FAIL")

