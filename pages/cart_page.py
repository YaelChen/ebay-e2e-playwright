from pages.base_page import BasePage
from playwright.sync_api import Page
import re


class CartPage(BasePage):
    """shopping cart page class"""
    
    CART_URL = "https://cart.ebay.com/sc/view"
    SUBTOTAL = "div[data-test-id='SUBTOTAL'] span.text-display-span"
    CART_ITEMS = "div.cart-bucket"
    ITEM_PRICE = "div[data-test-id='ITEM_PRICE'] span"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def open(self) -> None:
        """Open the cart page"""
        self.navigate_to(self.CART_URL)
        self.wait_for_load()
    
    def get_subtotal(self) -> float:
        """get cart subtotal as float"""
        try:
            total_text = self.get_text(self.SUBTOTAL)
            clean = re.sub(r'[^\d.]', '', total_text)
            return float(clean)
        except:
            return 0.0
    
    def get_items_count(self) -> int:
        """get items count in cart"""
        return self.page.locator(self.CART_ITEMS).count()