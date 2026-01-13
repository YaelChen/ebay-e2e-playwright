from pages.base_page import BasePage
from playwright.sync_api import Page


class ItemPage(BasePage):
    """ItemPage class for eBay item detail page"""
    
    ADD_TO_CART_BTN = "a[href*='AddToCart'], a:has-text('Add to cart')"
    VARIANT_SELECT = "select[aria-label*='Select']"
    ITEM_PRICE = "div.x-price-primary span.ux-textspans"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def select_first_variant_if_exists(self) -> None:
        """choose first variant option if variants exist"""
        selects = self.page.locator(self.VARIANT_SELECT).all()
        for select in selects:
            try:
                # Choose first option (index 1, index 0 is placeholder)
                select.select_option(index=1)
            except:
                pass
    
    def add_to_cart(self) -> bool:
        """Add item to cart"""
        try:
            # choose variants if any
            self.select_first_variant_if_exists()

            # click Add to Cart
            if self.is_visible(self.ADD_TO_CART_BTN):
                self.click(self.ADD_TO_CART_BTN)
                self.wait_for_load()
                return True
        except Exception as e:
            print(f"✗ Could not add to cart: {e}")
        
        return False
    
    def get_price(self) -> float:
        """get item price as float"""
        try:
            price_text = self.get_text(self.ITEM_PRICE)
            import re
            clean = re.sub(r'[^\d.]', '', price_text) #regex to keep digits and dot only
            return float(clean)
        except:
            return 0.0