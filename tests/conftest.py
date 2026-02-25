import os
import sys
import pytest
from dotenv import load_dotenv
# För ui testerna med Playwright
import time
from playwright.sync_api import sync_playwright

from src.POM_pages.base_page import BasePage
from src.POM_pages.personuppgifter_sida import Personuppgifter
from src.POM_pages.inkomstuppgifter_sida import Inkomstuppgifter
from src.POM_pages.laneuppgifter_sida import Laneuppgifter


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
def base_sida(page):
    return BasePage(page)

@pytest.fixture
def personuppgifter_page(page):
    return Personuppgifter(page)

@pytest.fixture
def inkomstuppgifter_page(page):
    return Inkomstuppgifter(page)

@pytest.fixture
def laneuppgifter_page(page):
    return Laneuppgifter(page)