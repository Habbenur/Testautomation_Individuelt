from __future__ import annotations
from playwright.sync_api import Page
from faker import Faker
from src.helpers.skattaverket_testdata import  SkatteverketTestdataClient
import re
import random
fake = Faker("sv_SE")

def to_ui_personnummer(pnr: str) -> str:
    """Skatteverket pnr -> UI format (YYYYMMDDXXXX or YYMMDDXXXX)."""
    digits = re.sub(r"\D", "", pnr)
    if len(digits) == 12:  # YYYYMMDDXXXX
        return f"{digits[:8]}{digits[8:]}"  # YYYYMMDDXXXX
    if len(digits) == 10:  # YYMMDDXXXX
        return f"{digits[:6]}{digits[6:]}"  # YYMMDDXXXX
    raise ValueError(f"Unexpected personnummer: {pnr}")

class Personuppgifter:
    def __init__(self, page: Page):
        self.page = page
        self.faker = Faker("sv_SE")  # Svensk lokal för fejkdata
        self.skv = SkatteverketTestdataClient(timeout_s=20.0)
  

    def personuppgifter_form(self):
        # test personnummer från Skatteverket
        offset = random.randint(0, 5000)
        pnrs = self.skv.get_test_personnummer(limit=1, offset=offset)
        if not pnrs:
            raise RuntimeError("Skatteverket returned no testpersonnummer.")
        self.personnummer_ui = to_ui_personnummer(pnrs[0])

        digits = re.sub(r"\D", "", self.personnummer_ui)
        # UI format: ÅÅMMDDXXXX (sista 10 digit)
        pnr_ui = digits[-10:]

        data = {
        "pnr": pnr_ui,
        "first_name": self.faker.first_name(),
        "last_name": self.faker.last_name(),
        "email": self.faker.email(),
        "phone": self.faker.phone_number(),
        "address": self.faker.street_address(),
        "postcode": self.faker.postcode(),
        "city": self.faker.city()
    }

        self.page.get_by_role("textbox", name="Personnummer *").fill(data["pnr"])
        self.page.get_by_role("textbox", name="Förnamn *").fill(data["first_name"])
        self.page.get_by_role("textbox", name="Efternamn *").fill(data["last_name"])
        self.page.get_by_role("textbox", name="E-post *").fill(data["email"])
        self.page.get_by_role("textbox", name="Telefonnummer *").fill(data["phone"])
        self.page.get_by_role("textbox", name="Adress *").fill(data["address"])
        self.page.get_by_role("textbox", name="Postnummer *").fill(data["postcode"])
        self.page.get_by_role("textbox", name="Stad *").fill(data["city"])
        return data

    def submit_personuppgifter(self) -> None: 
        self.page.get_by_role("button", name="Nästaä").click()

        