from playwright.sync_api import Page, expect
from typing import Optional
import time


class BasePage:
    """
    Base Page that all pages inherit from.
    has common methods for all pages.
    """
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate_to(self, url: str) -> None:
        """Navigate to a URL"""
        self.page.goto(url, wait_until="domcontentloaded")
    
    def click(self, selector: str, timeout: int = 30000) -> None:
        """Click on an element"""
        self.page.click(selector, timeout=timeout)
    
    def fill(self, selector: str, text: str) -> None:
        """Fill a field with text"""
        self.page.fill(selector, text)
    
    def get_text(self, selector: str) -> str:
        """Get text from an element"""
        return self.page.locator(selector).inner_text()
    
    def wait_for_selector(self, selector: str, timeout: int = 30000) -> None:
        """Wait for an element"""
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Check if an element is visible"""
        try:
            self.page.wait_for_selector(selector, timeout=timeout, state="visible")
            return True
        except:
            return False
    
    def get_current_url(self) -> str:
        """Get current URL"""
        return self.page.url
    
    def screenshot(self, name: str) -> str:
        """Take a screenshot"""
        path = f"reports/screenshots/{name}.png"
        self.page.screenshot(path=path)
        return path
    
    def scroll_to_element(self, selector: str) -> None:
        """Scroll to an element"""
        self.page.locator(selector).scroll_into_view_if_needed()
    
    def wait_for_load(self) -> None:
        """Wait for page load"""
        self.page.wait_for_load_state("networkidle")