from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BTN = (By.ID, "checkout")

    def get_items_count(self):
        try:
            return len(self.find_all(self.CART_ITEMS))
        except Exception:
            return 0

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BTN)