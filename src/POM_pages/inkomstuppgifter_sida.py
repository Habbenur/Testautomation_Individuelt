from __future__ import annotations
import random
from playwright.sync_api import Page, expect
from faker import Faker
from src.POM_pages.base_page import BasePage
fake = Faker("sv_SE")
BASE_URL = "https://souderbroder-loan-lab.lovable.app"

class Inkomstuppgifter(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.faker = Faker("sv_SE")  # Svensk lokal för fejkdata

    def inkomstuppgifter_form(self):
        data = {
        "income": str(random.randint(20000, 100000)),  # Generera en slumpmässig månadsinkomst mellan 20 000 och 100 000 SEK
        "employment_type": "Tillsvidareanställd",
        "employer": self.faker.company(),
        "side_income": "0"
    }
        income_input = self.page.get_by_role("spinbutton", name="Månadsinkomst (SEK) *")
        income_input.fill(data["income"])
        expect(income_input).to_have_value(data["income"])
        self.page.get_by_role("combobox", name="Anställningsform *").click()
        self.page.get_by_text(data["employment_type"]).click()
        self.page.get_by_role("textbox", name="Arbetsgivare *").fill(data["employer"])
        self.page.get_by_role("spinbutton", name="Sidoinkomst (SEK/månad)").fill(data["side_income"])
        return data
    def submit_inkomstuppgifter(self):
        self.page.get_by_role("button", name="Nästa").click()