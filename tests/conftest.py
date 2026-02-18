import os
import sys
import pytest
from dotenv import load_dotenv
# För ui testerna med Playwright
import time
from playwright.sync_api import sync_playwright

from src.helpers import SoderBroderLoan


# ─────────────────────────────────────────────
# Körs en gång när pytest-sessionen startar
# Laddar miljövariabler från .env-filen
# ─────────────────────────────────────────────
def pytest_sessionstart(session):
    load_dotenv()

@pytest.fixture()
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Sätt headless=True för att köra utan UI
        page = browser.new_page()
        yield page
        browser.close()


@pytest.fixture
def loan_page(page):
    loan = SoderBroderLoan(page)
    loan.goto()
    return loan
