from playwright.sync_api import expect
from src.POM_pages.base_page import BasePage
from src.POM_pages.personuppgifter_sida import Personuppgifter
from src.POM_pages.inkomstuppgifter_sida import Inkomstuppgifter
from src.POM_pages.laneuppgifter_sida import Laneuppgifter

def test_brollop_full_loan_flow(shared_page):
    base = BasePage(shared_page)
    base.goto()
    base.assert_title_is_correct()
    base.brollop_loan()

    pu = Personuppgifter(shared_page)
    data = pu.personuppgifter_form()
    expect(shared_page.get_by_role("textbox", name="Personnummer *")).to_have_value(data["pnr"])  # Kontrollera att personnumret är ifyllt
    expect(shared_page.get_by_role("textbox", name="Förnamn")).to_have_value(data["first_name"])  # Kontrollera att förnamnet är ifyllt
    expect(shared_page.get_by_role("textbox", name="Efternamn")).to_have_value(data["last_name"])  # Kontrollera att efternamnet är ifyllt
    expect(shared_page.get_by_role("textbox", name="E-post")).to_have_value(data["email"])  # Kontrollera att e-posten är ifyllt
    expect(shared_page.get_by_role("textbox", name="Telefonnummer")).to_have_value(data["phone"])  # Kontrollera att telefonnumret är ifyllt
    expect(shared_page.get_by_role("textbox", name="Adress")).to_have_value(data["address"])  # Kontrollera att adressen är ifyllt
    expect(shared_page.get_by_role("textbox", name="Postnummer")).to_have_value(data["postcode"])  # Kontrollera att postnumret är ifyllt
    expect(shared_page.get_by_role("textbox", name="Stad *")).to_have_value(data["city"])  # Kontrollera att orten är ifyllt
    pu.submit_personuppgifter() 

    ip = Inkomstuppgifter(shared_page)
    income_data = ip.inkomstuppgifter_form()
    expect(shared_page.get_by_label("Månadsinkomst (SEK) *")).to_have_value(income_data["income"])
    expect(shared_page.get_by_role("textbox", name="Arbetsgivare *")).to_have_value(income_data["employer"])
    expect(shared_page.get_by_role("spinbutton", name="Sidoinkomst (SEK/månad)")).to_have_value(income_data["side_income"])
    ip.submit_inkomstuppgifter()

    lp = Laneuppgifter(shared_page)
    loan_data = lp.laneuppgifter_form(amount=200000)
    expect(shared_page.get_by_role("spinbutton", name="Lånebelopp (SEK) *")).to_have_value(str(loan_data["amount"]))
    lp.submit_laneuppgifter()

    expect(shared_page.get_by_text("Din låneansökan är mottagen")).to_be_visible()