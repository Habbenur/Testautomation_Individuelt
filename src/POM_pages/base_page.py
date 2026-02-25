from __future__ import annotations
import re
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

    def bil_loan(self):
        self.page.get_by_role("img").nth(1).click()
        self.page.get_by_role("button", name="Nästa").click()
        expect(self.page.get_by_label(re.compile(r"Personnummer", re.I))).to_be_visible()
    
    def boat_loan(self):
        self.page.get_by_text("BåtSjösätt dina planer").click()
        self.page.get_by_role("button", name="Nästa").click()
        expect(self.page.get_by_label(re.compile(r"Personnummer", re.I))).to_be_visible()

    def brollop_loan(self):
        self.page.get_by_text("BröllopDen stora dagen").click()
        self.page.get_by_role("button", name="Nästa").click()
        expect(self.page.get_by_label(re.compile(r"Personnummer", re.I))).to_be_visible()

    def renoverings_loan(self):
        self.page.get_by_text("RenoverringFörnya ditt hem").click()
        self.page.get_by_role("button", name="Nästa").click()
        expect(self.page.get_by_label(re.compile(r"Personnummer", re.I))).to_be_visible()

    def semester_loan(self):
        self.page.get_by_text("SemesterÄventyr väntar").click()
        self.page.get_by_role("button", name="Nästa").click()
        expect(self.page.get_by_label(re.compile(r"Personnummer", re.I))).to_be_visible()