from pages.base_page import BasePage
from playwright.sync_api import Page
from typing import List
import re


class SearchResultsPage(BasePage):
    """SearchResultsPage class for eBay search results page"""
    
    # Locators
    RESULTS_LIST = "ul.srp-results li.s-item"
    ITEM_TITLE = "div.s-item__title span"
    ITEM_PRICE = "span.s-item__price"
    ITEM_LINK = "a.s-item__link"
    
    # Price filter
    PRICE_MIN = "input[aria-label='Minimum Value']"
    PRICE_MAX = "input[aria-label='Maximum Value']"
    PRICE_SUBMIT = "button[aria-label='Submit price range']"
    
    # Pagination
    NEXT_BUTTON = "a.pagination__next"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def apply_price_filter(self, max_price: float) -> None:
        """filter results by max price (0 - max_price)"""
        if self.is_visible(self.PRICE_MIN):
            self.fill(self.PRICE_MIN, "0")
            self.fill(self.PRICE_MAX, str(int(max_price)))
            self.click(self.PRICE_SUBMIT)
            self.wait_for_load()
    
    def get_item_urls_under_price(self, max_price: float, limit: int) -> List[str]:
        """get item URLs with price under max_price, up to limit"""
        urls = []

        # Wait for results to load
        self.wait_for_selector(self.RESULTS_LIST)
        
        #Get all items
        items = self.page.locator(self.RESULTS_LIST).all()
        
        for item in items:
            if len(urls) >= limit:
                break
            
            try:
                # get price text and convert to float
                price_text = item.locator(self.ITEM_PRICE).inner_text()
                price = self._extract_price(price_text)
                
                # if the price is under max_price, get the URL
                if price > 0 and price <= max_price:
                    url = item.locator(self.ITEM_LINK).get_attribute("href")
                    if url and url not in urls:
                        urls.append(url)
                        print(f"✓ Found item: ${price} - {url[:50]}...")
            except Exception as e:
                continue
        
        return urls
    
    def _extract_price(self, price_text: str) -> float:
        """clean price text"""
        # remove $, commas, etc.
        # if there's "to" (range) - take the first one
        clean = price_text.split(" to ")[0]
        clean = re.sub(r'[^\d.]', '', clean) # regex to keep digits and dot only
        
        try:
            return float(clean)
        except:
            return 0.0
    
    def has_next_page(self) -> bool:
        """Check if there's a next page"""
        return self.is_visible(self.NEXT_BUTTON)
    
    def go_to_next_page(self) -> None:
        """go to next page if exists"""
        if self.has_next_page():
            self.click(self.NEXT_BUTTON)
            self.wait_for_load()