Dfrom pages.base_page import BasePage
from playwright.sync_api import Page


class LoginPage(BasePage):
    """LoginPage class for eBay login page"""
    
    # locators
    SIGNIN_LINK = "a[href*='signin']"
    EMAIL_INPUT = "#userid"
    PASSWORD_INPUT = "#pass"
    SIGNIN_BUTTON = "#sgnBt"
    ERROR_MESSAGE = "#errMsg"
    USER_ID_HEADER = "#gh-ug"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://signin.ebay.com/"
    
    def open(self) -> None:
        """Open the login page"""
        self.navigate_to(self.url)
    
    def login(self, email: str, password: str) -> None:
        """Perform login action with given credentials"""
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.SIGNIN_BUTTON)
        self.wait_for_load()
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in by verifying the presence of user ID header"""
        return self.is_visible(self.USER_ID_HEADER)
    
    def get_error_message(self) -> str:
        """Get error message"""
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""