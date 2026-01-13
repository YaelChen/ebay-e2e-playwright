from pages.base_page import BasePage
from playwright.sync_api import Page


class HomePage(BasePage):
    """HomePage class for eBay home page"""
    
    SEARCH_BOX = "#gh-ac"
    SEARCH_BUTTON = "#gh-search-btn"
    LOGO = "#gh-logo"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://www.ebay.com"
    
    def open(self) -> None:
        """Open the home page"""
        self.navigate_to(self.url)
        self.wait_for_selector(self.SEARCH_BOX)
    
    def search(self, search_term: str) -> None:
        """Search for an item"""
        self.fill(self.SEARCH_BOX, search_term)
        self.click(self.SEARCH_BUTTON)
        self.wait_for_load()