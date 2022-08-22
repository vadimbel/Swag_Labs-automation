import time
from base.base_actions import BaseActions
from base.logger import customLogger
from page.login_page import LoginPage


class Navigation(BaseActions):
    """
    This class created to navigate through different webpages
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    log = customLogger()

    # valid user info to successfully login to webpage
    VALID_USER_NAME = "standard_user"
    VALID_PASSWORD = "secret_sauce"

    # pages :
    BASE_URL = "https://www.saucedemo.com/"
    PRODUCT_URL = "https://www.saucedemo.com/inventory.html"
    YOUR_CART_URL = "https://www.saucedemo.com/cart.html"
    YOUR_INFORMATION_URL = "https://www.saucedemo.com/checkout-step-one.html"
    CHECKOUT_OVERVIEW_URL = "https://www.saucedemo.com/checkout-step-two.html"
    FINAL_URL = "https://www.saucedemo.com/checkout-complete.html"

    # types
    cart_icon_type = "class"
    checkout_type = "xpath"
    first_name_type = "id"
    last_name_type = "id"
    code_type = "id"
    continue_button_type = "id"

    # locators
    cart_icon_locator = "shopping_cart_container"
    checkout_locator = '//button[@id="checkout"]'
    first_name_locator = "first-name"
    last_name_locator = "last-name"
    code_locator = "postal-code"
    continue_button_locator = "continue"

    def navigate_to_product_page(self):
        """
        This method will navigate from 'login' page to 'product' page .
        :return: None
        """
        # login - using 'LoginPage' of 'login_page' module
        lg = LoginPage(self.driver)
        lg.login(self.VALID_USER_NAME, self.VALID_PASSWORD)

        # check if logged in successfully - reached to product page
        if self.driver.current_url == self.PRODUCT_URL:
            self.navigation_message("PRODUCT PAGE", 1)
            return True
        else:
            self.navigation_message("PRODUCT PAGE", 2)
            return False

    def navigate_to_your_cart_page(self):
        """
        This method will navigate :
        from 'product' page -> 'your cart' page .
        :return: None
        """
        # find and click 'cart icon'
        self.click_element(self.cart_icon_type, self.cart_icon_locator)

        # check if reached to 'your cart page'
        if self.driver.current_url == self.YOUR_CART_URL:
            self.navigation_message("YOUR CART PAGE", 1)
            return True
        else:
            self.navigation_message("YOUR CART PAGE", 2)
            return False

    def navigate_to_your_information_page(self):
        """
        This method will navigate :
        from 'your cart' page -> 'information' page .
        :return: None
        """
        # find 'checkout' button and click it , then check if reached to 'your information' page
        self.click_element(self.checkout_type, self.checkout_locator)

        if self.driver.current_url == self.YOUR_INFORMATION_URL:
            self.navigation_message("YOUR INFORMATION PAGE", 1)
            return True
        else:
            self.navigation_message("YOUR INFORMATION PAGE", 2)
            return False

    def navigate_to_overview_page_from_product_page(self):
        """
        This method will navigate :
        from 'product' page -> 'overview' page .
        :return:
        """
        # from 'product' page -> navigate to 'your cart' page
        self.navigate_to_your_cart_page()

        # from 'your cart' page -> navigate to 'information' page
        self.navigate_to_your_information_page()

        # enter keys to 3 text fields on 'information' page
        self.enter_key_to_field(self.first_name_type, self.first_name_locator, "a")
        self.enter_key_to_field(self.last_name_type, self.last_name_locator, "a")
        self.enter_key_to_field(self.code_type, self.code_locator, "a")

        # then click 'continue' to reach 'overview' page
        self.click_element(self.continue_button_type, self.continue_button_locator)

        # check if reached to 'overview' page
        if self.driver.current_url == self.CHECKOUT_OVERVIEW_URL:
            self.navigation_message("OVERVIEW PAGE", 1)
            return True
        else:
            self.navigation_message("OVERVIEW PAGE", 2)
            return False

    def navigation_message(self, name: str, option: int):
        """
        This method update log if navigation passed successfully/failed .
        if failed -> update log & take screenshot .
        if passed -> update log .
        :param name: name of page .
        :param option: pass/fail .
        :return: None
        """
        if option == 1:
            self.log.info(f"### NAVIGATION - MOVED TO : {name} - SUCCESSFULLY - VALID ###")
        elif option == 2:
            self.take_screenshot()
            self.log.error(f"### NAVIGATION - CANNOT REACH : {name} - INVALID")
        else:
            self.log.error("### INVALID OPTION !")
