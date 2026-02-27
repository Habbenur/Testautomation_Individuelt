from __future__ import annotations
from playwright.sync_api import Page, expect

class Laneuppgifter:
    def __init__(self, page: Page):
        self.page = page

    def laneuppgifter_form(self, amount: int) -> dict:
        data = {"amount": amount}

        amount_input = self.page.get_by_role(
            "spinbutton",
            name="Lånebelopp (SEK) *"
        )

        # Simulera riktig användarinput
        amount_input.click()
        amount_input.press("Meta+A")   # Mac
        amount_input.type(str(amount), delay=20)
        amount_input.blur()

        # Verifiera att det inskrivna värdet är korrekt
        expect(amount_input).to_have_value(str(amount))

    
        self.page.get_by_role("slider").click()
        self.page.locator(".relative.h-2").click()

        self.page.get_by_role(
            "button",
            name="Beräkna månadskostnad"
        ).click()

        expect(
            self.page.get_by_text("Totalt att betala:")
        ).to_be_visible()

        return data

    def submit_laneuppgifter(self):
        self.page.get_by_role("button", name="Nästa").click()
        self.page.get_by_role("button", name="Skicka ansökan").click()