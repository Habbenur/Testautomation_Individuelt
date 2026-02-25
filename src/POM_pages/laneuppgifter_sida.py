from __future__ import annotations
from playwright.sync_api import Page, expect
from faker import Faker
fake = Faker("sv_SE")
BASE_URL = "https://souderbroder-loan-lab.lovable.app"

class Laneuppgifter:
    def __init__(self, page: Page):
        self.page = page

    def laneuppgifter_form(self, amount: int) -> dict:
        data = {
            "amount": amount,
        }
        amount_input = self.page.get_by_role("spinbutton", name="Lånebelopp (SEK) *")
        amount_input.fill(str(data["amount"]))
        expect(amount_input).to_have_value(str(data["amount"]))

        self.page.get_by_role("slider").click()
        self.page.locator(".relative.h-2").click()

        self.page.get_by_role("button", name="Beräkna månadskostnad").click()
        expect(self.page.get_by_text("Totalt att betala:")).to_be_visible()
        self.page.get_by_text("Totalt att betala:").click()
        
        return data
    
    def submit_laneuppgifter(self):
        self.page.get_by_role("button", name="Nästa").click()
        self.page.get_by_role("button", name="Skicka ansökan").click() 