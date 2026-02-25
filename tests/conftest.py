import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

def pytest_sessionstart(session):
    load_dotenv()

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope="module")
def shared_page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()