from __future__ import annotations
from playwright.sync_api import Page, expect

BASE_URL = "https://souderbroder-loan-lab.lovable.app"

class BasePage:
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = BASE_URL

    def goto(self):
        #Öppna sidan.
        self.page.goto(BASE_URL)

    def assert_title_is_correct(self):
        expect(self.page.locator("h1")).to_have_text("Söderbröder Finans AB")