from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    FINISH_BTN = (By.ID, "finish")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def fill_information(self, first_name, last_name, postal_code):
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)
        
        # Scroll y clic usando self.driver directamente
        btn_continue = self.driver.find_element(*self.CONTINUE_BTN)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn_continue)
        try:
            self.click(self.CONTINUE_BTN)
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn_continue)

    def finish_order(self):
        # Scroll y clic usando self.driver directamente
        btn_finish = self.driver.find_element(*self.FINISH_BTN)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn_finish)
        try:
            self.click(self.FINISH_BTN)
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn_finish)

    def get_confirmation_message(self):
        return self.get_text(self.COMPLETE_HEADER)