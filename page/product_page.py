import time
from base.base_actions import BaseActions
from base.logger import customLogger


class ProductPage(BaseActions):
    """
    This module contains functions that will be used on 'product' page .
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # object of class 'customLogger' - to be able to write into the log when using function from this module
    _log = customLogger()

    # amount of items should appear on 'product' page
    ITEMS_AMOUNT = 6

    # locators type - of elements will be used on ' product' page
    items_type = "class"
    item_img_type = "xpath"
    item_label_type = "xpath"
    item_prices_type = "class"
    add_button_type = "xpath"
    remove_button_type = "xpath"
    cart_icon_type = "class"
    inventory_items_name_type = "xpath"
    inventory_items_price_type = "class"
    product_sort_container_type = "xpath"
    product_sort_options_type = "xpath"

    # locators - of elements will be used
    items_locator = "inventory_item"
    item_img_locator = '//div[@class="inventory_item_img"]'
    item_label_locator = '//div[@class="inventory_item_label"]'
    item_prices_locator = "inventory_item_price"
    add_button_locator = '//button[@class="btn btn_primary btn_small btn_inventory"]'
    remove_button_locator = "//button[@class='btn btn_secondary btn_small btn_inventory']"
    cart_icon_locator = "shopping_cart_badge"
    inventory_items_name_locator = '//div[@class="inventory_item_name"]'
    inventory_items_price_locator = "inventory_item_price"
    product_sort_container_locator = '//*[@id="header_container"]//select'
    product_sort_options_locator = '//*[@id="header_container"]/div[2]/div[2]/span/select/option[{}]'

    def count_items(self):
        """
        This method will be activated in 'test_count_items' test on 'product_tests' .
        find how many elements appear on 'product' page (items, images of item, labels of item,
        prices of item and buttons .
        :return:
        """
        test_name = "TEST_COUNT_ITEMS"

        # find and count how many items appear on the webpage
        items = self.get_elements(self.items_type, self.items_locator)
        count_items = self.check_count_elements(elements=items, amount=self.ITEMS_AMOUNT, test_name=test_name)

        # find and count how many images appear on the webpage
        imgs = self.get_elements(self.item_img_type, self.item_img_locator)
        count_img = self.check_count_elements(elements=imgs, amount=self.ITEMS_AMOUNT, test_name=test_name)

        # find and count labels
        labels = self.get_elements(self.item_img_type, self.item_label_locator)
        count_label = self.check_count_elements(elements=labels, amount=self.ITEMS_AMOUNT, test_name=test_name)

        # find and count prices
        prices = self.get_elements(self.item_prices_type, self.item_prices_locator)
        count_prices = self.check_count_elements(elements=prices, amount=self.ITEMS_AMOUNT, test_name=test_name)

        # find and count buttons
        buttons = self.get_elements(self.add_button_type, self.add_button_locator)
        count_buttons = self.check_count_elements(elements=buttons, amount=self.ITEMS_AMOUNT, test_name=test_name)

        # should be 'ITEMS_AMOUNT' items
        if not count_items or not count_img or not count_label or not count_prices or not count_buttons:
            self.test_fail(test_name)
            return False

        self.test_pass(test_name)
        return True

    def add_remove_items(self):
        """
        This method will be activated in 'test_add_remove_buttons' test on 'product_tests' .
        find all 'add to cart' buttons & click them , then check if elements added to 'cart' icon .
        afterwards finds all 'remove' button and click them . then check if all items removed from 'cart' icon .
        :return:
        """
        test_name = "TEST_ADD_REMOVE_BUTTONS"

        # find 'add to cart' buttons and click them
        self.click_elements(locator_type=self.add_button_type, locator=self.add_button_locator)

        # find cart icon and check if all items added
        cart_link = self.get_element(self.cart_icon_type, self.cart_icon_locator)

        if int(cart_link.text) != self.ITEMS_AMOUNT:
            self._log.error(f"### TEST - ITEMS ADDED : {cart_link.text} - SHOULD BE : {self.ITEMS_AMOUNT} - INVALID")
            self.test_fail("TEST_ADD_REMOVE_BUTTONS")
            return False

        self._log.info(f"### TEST - all items added : {cart_link} - valid")

        # find 'remove' buttons and click them
        self.click_elements(locator_type=self.remove_button_type, locator=self.remove_button_locator)

        # check if any 'remove' button exists (should not exist)
        buttons = self.is_element_present(self.remove_button_type, self.remove_button_locator)

        # if buttons is not False -> method above found 'remove' button .
        if buttons != False:
            self._log.error(f"TEST - NOT ALL ITEMS REMOVED FROM CART - INVALID")
            self.test_fail(test_name)
            return False

        self._log.info(f"TEST - all items removed - valid")
        self.test_pass(test_name)
        return True

    def sort_options(self, option):
        """
        This method used in 'test_order' test .
        finds the sorting element on 'product' webpage , then click it .
        then click on one of the sorting options - according to 'options' parameter .

        :param option: sorting order option .
        :return:
        """
        # finds the sorting element on 'product' page , then click it
        self.click_element(self.product_sort_container_type, self.product_sort_container_locator)

        # finds the sorting option , then clicks it
        self.click_element(self.product_sort_options_type, self.product_sort_options_locator.format(option))

    def check_sort_option(self, option):
        """
        This method used in 'test_order' test .
        tests the sorting functionality of chosen option .

        :param option: sorting option .
        :return:
        """
        start = 0

        # A - Z option - checks if the items on the main website appear in alphabetic order
        if int(option) == 1:
            self._log.info("### TESTING - option : A - Z")
            # get the 'names' of the elements on the website and put then in a list
            items_names = self.get_elements(self.inventory_items_name_type, self.inventory_items_name_locator)
            list_of_items = [item.text for item in items_names]

            # checks if all items are sorted by : A - Z
            while start < len(list_of_items) - 1:
                if list_of_items[start] > list_of_items[start + 1]:
                    self._log.error("CHOSEN SORT IS : A-Z --> TEST FAILED AT : {0} - {1}"
                                    .format(list_of_items[start], list_of_items[start + 1]))
                    return False
                else:
                    self._log.info(
                        "### TEST - {0} - {1} -- valid".format(list_of_items[start], list_of_items[start + 1]))
                    start += 1

        # Z - A option - checks if the items on the main website appear in the right alphabetic order
        elif int(option) == 2:
            self._log.info("### TESTING - option : Z - A")
            # get the 'names' of the elements on the website and put them in a list
            items_names = self.get_elements(self.inventory_items_name_type, self.inventory_items_name_locator)
            list_of_items = [item.text for item in items_names]

            # checks if all items are sorted by : Z - A
            while start < len(list_of_items) - 1:
                if list_of_items[start] < list_of_items[start + 1]:
                    self._log.error("CHOSEN SORT IS : Z-A --> TEST FAILED AT : {0} - {1}"
                                    .format(list_of_items[start], list_of_items[start + 1]))
                    return False
                else:
                    self._log.info(
                        "### TEST - {0} - {1} -- valid".format(list_of_items[start], list_of_items[start + 1]))
                    start += 1

        # price option - low to high - checks if item sorted by low to high prices
        elif int(option) == 3:
            self._log.info("### TESTING - option : price - low to high")
            # get 'prices' of the elements on the website and put them in a list
            items_names = self.get_elements(self.inventory_items_price_type, self.inventory_items_price_locator)
            list_of_items = [float(item.text[1:]) for item in items_names]

            # checks if all items are sorted by : prices - low to high
            while start < len(list_of_items) - 1:
                if list_of_items[start] > list_of_items[start + 1]:
                    self._log.error("CHOSEN PRICES SORT IS : LOW TO HIGH --> TEST FAILED AT : {0} - {1}"
                                    .format(list_of_items[start], list_of_items[start + 1]))
                    return False
                else:
                    self._log.info("### TEST - {0} =< {1} -- valid".format(list_of_items[start],
                                                                           list_of_items[start + 1]))
                    start += 1

        # price option - high to low - checks if item sorted by high to low prices
        elif int(option) == 4:
            self._log.info("### TESTING - option : price - high to low")
            # get 'prices' of the elements on the website and put them in a list
            items_names = self.get_elements(self.inventory_items_price_type, self.inventory_items_price_locator)
            list_of_items = [float(item.text[1:]) for item in items_names]

            # checks if all items are sorted by : prices - high to low
            while start < len(list_of_items) - 1:
                if list_of_items[start] < list_of_items[start + 1]:
                    self._log.error("CHOSEN PRICES SORT IS : HIGH TO LOW --> TEST FAILED AT : {0} - {1]"
                                    .format(list_of_items[start], list_of_items[start + 1]))
                    return False
                else:
                    self._log.info("### TEST - {0} >= {1} -- valid".format(list_of_items[start],
                                                                           list_of_items[start + 1]))
                    start += 1

        self.test_sort_pass_message(option)
        return True

    def test_pass(self, test_name):
        self._log.info(f"### TEST - {test_name} - PASSED .")

    def test_fail(self, test_name):
        self._log.error(f"### TEST - {test_name} - FAILED .")

    def test_sort_pass_message(self, option):

        if int(option) == 1:
            self._log.info("### TEST - sort by chosen order : A - Z - PASS .\n")
        elif int(option) == 2:
            self._log.info("### TEST - sort by chosen order : Z - A - PASS .\n")
        elif int(option) == 3:
            self._log.info("### TEST - sort by chosen price : low to high - PASS .\n")
        elif int(option) == 4:
            self._log.info("### TEST - sort by chosen price : high to low - PASS .\n")
        else:
            self._log.error("### INVALID OPTION ON SORTING TESTS .")

