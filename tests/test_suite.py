import unittest
from tests.login_tests import LoginTests
from tests.product_tests import ItemsTests
from tests.your_cart_tests import YourCartTests
from tests.your_info_tests import YourInfoTests
from tests.overview_tests import OverviewTests


# Get all tests from tests package
tc1 = unittest.TestLoader().loadTestsFromTestCase(LoginTests)
tc2 = unittest.TestLoader().loadTestsFromTestCase(ItemsTests)
tc3 = unittest.TestLoader().loadTestsFromTestCase(YourCartTests)
tc4 = unittest.TestLoader().loadTestsFromTestCase(YourInfoTests)
tc5 = unittest.TestLoader().loadTestsFromTestCase(OverviewTests)


# Create a test suite combining all tests from above
smokeTest = unittest.TestSuite([tc1, tc2, tc3, tc4, tc5])

# run all tests
unittest.TextTestRunner(verbosity=2).run(smokeTest)
