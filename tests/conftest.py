import pytest
from playwright.sync_api import Browser, BrowserContext, Page
import json
import os


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Session level settings - once for all the tests
    """
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
        "locale": "en-US",
    }


@pytest.fixture(scope="function")
def page(browser: Browser):
    """
    Fixture that creates a new Page for eace test.
    """
    context = browser.new_context()
    page = context.new_page()
    
    yield page  # The test runs here
    
    # Cleanup after test
    page.close()
    context.close()


@pytest.fixture(scope="session")
def test_data():
    """
    Loading test data from JSON
    scope="session" = loads once per run
    """
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "test_data.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def pytest_configure(config):
    """
    Create reports/screenshots directory if it doesn't exist
    """
    screenshots_dir = "reports/screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)