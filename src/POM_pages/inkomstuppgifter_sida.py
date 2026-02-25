from __future__ import annotations
from playwright.sync_api import Page
from faker import Faker
from src.POM_pages.base_page import BasePage
from src.POM_pages.personuppgifter_sida import Personuppgifter
fake = Faker("sv_SE")
BASE_URL = "https://souderbroder-loan-lab.lovable.app"

class Inkomstuppgifter(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.faker = Faker("sv_SE")  # Svensk lokal för fejkdata

    def inkomstuppgifter_form(self):
        personuppgifter_page = Personuppgifter(self.page)
        personuppgifter_page.personuppgifter_form()
        personuppgifter_page.submit_personuppgifter()

        data = {
        "income": "30000",
        "employment_type": "Tillsvidareanställd",
        "employer": self.faker.company(),
        "side_income": "0"
    }
        self.page.get_by_label("Månadsinkomst (SEK) *").fill(data["income"])
        self.page.get_by_role("combobox", name="Anställningsform *").click()
        self.page.get_by_text(data["employment_type"]).click()
        self.page.get_by_role("textbox", name="Arbetsgivare *").fill(data["employer"])
        self.page.get_by_role("spinbutton", name="Sidoinkomst (SEK/månad)").fill(data["side_income"])
        return data
    def submit_inkomstuppgifter(self):
        self.page.get_by_role("button", name="Nästa").click()