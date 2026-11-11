from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

class InventoryPage(BasePage):
    URL_PATH = "/inventory.html"

    # Locators
    PAGE_TITLE = (By.CLASS_NAME, "title")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    ADD_BACKPACK_BTN = (By.ID, "add-to-cart-sauce-labs-backpack")
    REMOVE_BACKPACK_BTN = (By.ID, "remove-sauce-labs-backpack")

    def is_loaded(self):
        return self.URL_PATH in self.get_current_url() and self.find_visible(self.PAGE_TITLE).is_displayed()

    def get_title_text(self):
        return self.get_text(self.PAGE_TITLE)

    def add_backpack_to_cart(self):
        self.click(self.ADD_BACKPACK_BTN)

    def remove_backpack_from_cart(self):
        self.click(self.REMOVE_BACKPACK_BTN)

    def get_cart_badge_count(self):
        try:
            return int(self.get_text(self.CART_BADGE))
        except Exception:
            return 0

    def go_to_cart(self):
        self.click(self.CART_LINK)

    def sort_by(self, value):
        """Valores posibles: 'lohi', 'hilo', 'az', 'za'"""
        select = Select(self.find_visible(self.SORT_DROPDOWN))
        select.select_by_value(value)

    def get_all_prices(self):
        elements = self.find_all(self.ITEM_PRICES)
        return [float(elem.text.replace("$", "")) for elem in elements]