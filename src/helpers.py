from encodings.punycode import digits
from multiprocessing import context
from playwright.sync_api import Page, expect
from faker import Faker
from src.skattaverket_testdata import  SkatteverketTestdataClient
import re
import random
fake = Faker("sv_SE")
BASE_URL = "https://souderbroder-loan-lab.lovable.app"

def to_ui_personnummer(pnr: str) -> str:
    """Skatteverket pnr -> UI format (YYYYMMDDXXXX or YYMMDDXXXX)."""
    digits = re.sub(r"\D", "", pnr)
    if len(digits) == 12:  # YYYYMMDDXXXX
        return f"{digits[:8]}{digits[8:]}"  # YYYYMMDDXXXX
    if len(digits) == 10:  # YYMMDDXXXX
        return f"{digits[:6]}{digits[6:]}"  # YYMMDDXXXX
    raise ValueError(f"Unexpected personnummer: {pnr}")

class SoderBroderLoan:

    def __init__(self, page: Page):
        self.page = page
        self.faker = Faker("sv_SE")  # Svensk lokal för fejkdata
        self.skv = SkatteverketTestdataClient(timeout_s=20.0)

    def goto(self):
        """Öppna sidan."""
        self.page.goto(BASE_URL)
        offset = random.randint(0, 5000)
        pnrs = self.skv.get_test_personnummer(limit=1, offset=offset)
        if not pnrs:
            raise RuntimeError("Skatteverket returned no testpersonnummer.")
        self.personnummer_ui = to_ui_personnummer(pnrs[0])
    
    def fill_loan_form(self, amount: int, term: int):
        self.page.get_by_role("img").nth(1).click()
        self.page.get_by_role("button", name="Nästa").click()
        digits = re.sub(r"\D", "", self.personnummer_ui)
        # UI format: ÅÅMMDDXXXX (sista 10 digit)
        pnr_ui = digits[-10:]
        self.page.get_by_role("textbox", name="Personnummer *").fill(pnr_ui)
        self.page.get_by_role("textbox", name="Förnamn *").fill(self.faker.first_name())
        self.page.get_by_role("textbox", name="Efternamn *").fill(self.faker.last_name())
        self.page.get_by_role("textbox", name="E-post *").fill(self.faker.email())
        self.page.get_by_role("textbox", name="Telefonnummer *").fill(self.faker.phone_number())
        self.page.get_by_role("textbox", name="Adress *").fill(self.faker.street_address())
        self.page.get_by_role("textbox", name="Postnummer *").fill(self.faker.postcode())
        self.page.get_by_role("textbox", name="Stad *").fill(self.faker.city())
        self.page.get_by_role("button", name="Nästaä").click()
        self.page.get_by_label("Månadsinkomst (SEK) *").fill("30000")
        self.page.get_by_role("spinbutton", name="Månadsinkomst (SEK) *").fill("30000")
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


