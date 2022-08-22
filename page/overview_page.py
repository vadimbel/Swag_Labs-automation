from base.base_actions import BaseActions
from base.logger import customLogger


class OverviewPage(BaseActions):
    """
        This module contains functions that will be used on 'checkout overview' page .
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # object of class 'customLogger' - to be able to write into the log when using function from this module
    _log = customLogger()

    # types
    add_button_type = "xpath"
    price_type = "xpath"
    tax_type = "xpath"
    total_type = "xpath"

    # locators
    add_button_locator = '//button[@class="btn btn_primary btn_small btn_inventory"]'
    price_locator = "//div[@class='inventory_item'][{}]//div[@class='inventory_item_price']"
    tax_locator = "//div[@class='summary_tax_label']"
    total_locator = "//div[@class='summary_total_label']"

    def add_items(self, amount):
        """
        This method will be activated on 'test_total_sum' test from 'overview_page' file .
        on 'product' page , finds first 'amount' 'add to cart' button and click them -> add first 'amount' items to
        cart . then gets the prices of the items were clicked and return the sum of the prices .

        :param amount: amount of items will be added to cart .
        :return: sum of prices .
        """
        test_name = "TEST_TOTAL_SUM"
        total_sum = 0

        # find 'add to cart' buttons and click the first 'amount' of them
        buttons = self.get_elements(self.add_button_type, self.add_button_locator)
        for i in range(0, amount):
            self.click_element(element=buttons[i])

        # get the prices of the first 'amount' items were clicked above
        for i in range(0, amount):
            price = self.get_element(self.price_type, self.price_locator.format(i+1)).text
            self._log.info(f"Add : {price}")
            total_sum += float(price[1:])

        # return the sum
        self._log.info(f"### RETURN TOTAL_SUM = {total_sum}")
        return total_sum

    def check_item_total(self, total_sum):
        """
        This method will be activated on 'test_total_sum' test from 'overview_tests' file .
        on 'overview' page :
        1. finds 'Item total' element and check if price displayed is valid (equals to 'total_sum') .
        2. finds 'Tax' element and get tax fee displayed on page and adds it to 'total_sum' .
        3. finds 'Total' element and get fee displayed on page and check if the sum displayed is correct .

        :param total_sum: sum of the items were added from 'product' page .
        :return:
        """
        test_name = "TEST_TOTAL_SUM"

        # on 'overview' page , get 'item total' element
        item_total = self.get_element("xpath", "//div[@class='summary_subtotal_label']")
        item_total_fee = float(item_total.text[13:])

        # check if 'total_sum' == item total appear on 'overview' page
        if total_sum != item_total_fee:
            self._log.error(f"### TEST - {test_name} - total_sum is : {total_sum} ,"
                            f" item_total is : {item_total_fee} - INVALID")
            self.test_pass_message(test_name)
            return False

        # get 'Tax' fee and add it to 'total_sum'
        tax = self.get_element(self.tax_type, self.tax_locator)
        tax_fee = float(tax.text[6:])
        self._log.info(f"tax = {tax_fee}")
        total_sum += tax_fee

        # get 'Total' fee and check if 'total_sum' == 'Total' fee
        total = self.get_element(self.total_type, self.total_locator)
        total_fee = float(total.text[8:])
        self._log.info(f"total = {total_fee}")

        if total_fee != total_sum:
            self._log.error(f"### TEST - {test_name} - total_sum is : {total_sum} ,"
                            f"Total is : {total_fee} - INVALID")
            self.test_fail_message(test_name)
            return False

        self._log.info(f"### TEST - {test_name} - total_sum is : {total_sum}, item total is : {item_total_fee} , "
                       f"tax is : {tax_fee} , total is : {total_fee} - VALID")
        self.test_pass_message(test_name)
        return True

    def test_pass_message(self, test_name):
        self._log.info(f"### TEST - {test_name} - PASSED")

    def test_fail_message(self, test_name):
        self.take_screenshot()
        self._log.error(f"### TEST - {test_name} - INVALID")







