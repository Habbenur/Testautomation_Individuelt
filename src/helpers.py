from multiprocessing import context
from playwright.sync_api import Page, expect
from faker import Faker
import pytest

BASE_URL = "https://souderbroder-loan-lab.lovable.app"

class SoderBroderLoan:
    
    def __init__(self, page: Page):
        self.page = page
        self.faker = Faker("sv_SE")  # Svensk lokal för fejkdata

    def goto(self):
        """Öppna sidan."""
        self.page.goto(BASE_URL)
    
    def fill_loan_form(self, amount: int, term: int):
        self.page.get_by_role("img").nth(1).click()
        self.page.get_by_role("button", name="Nästa").click()
        self.page.get_by_role("textbox", name="Personnummer *").fill(self.faker.ssn())
        self.page.get_by_role("textbox", name="Förnamn *").fill(self.faker.first_name())
        self.page.get_by_role("textbox", name="Efternamn *").fill(self.faker.last_name())
        self.page.get_by_role("textbox", name="E-post *").fill(self.faker.email())
        self.page.get_by_role("textbox", name="Telefonnummer *").fill(self.faker.phone_number())
        self.page.get_by_role("textbox", name="Adress *").fill(self.faker.address())
        self.page.get_by_role("textbox", name="Postnummer *").fill(self.faker.postcode())
        self.page.get_by_role("textbox", name="Stad *").fill(self.faker.city())
        self.page.get_by_role("button", name="Nästaä").click()
        self.page.get_by_role("spinbutton", name="Månadsinkomst (SEK) *").fill(str(self.faker.random_int(min=20000, max=100000)))
        self.page.get_by_role("combobox", name="Anställningsform *").click()
        self.page.get_by_text("Tillsvidareanställd").click()
        self.page.get_by_role("textbox", name="Arbetsgivare *").fill(self.faker.company())
        self.page.get_by_role("spinbutton", name="Sidoinkomst (SEK/månad)").fill("0")
        self.page.get_by_role("button", name="Nästa").click()
        self.page.get_by_role("spinbutton", name="Lånebelopp (SEK) *").fill(str(amount))
        self.page.get_by_role("slider").click()
        self.page.locator(".relative.h-2").click()
        self.page.get_by_role("button", name="Beräkna månadskostnad").click()
        self.page.get_by_text("Totalt att betala:").click()
        self.page.get_by_role("button", name="Nästa").click()
        self.page.get_by_role("button", name="Skicka ansökan").click()  


