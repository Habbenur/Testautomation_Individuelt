from playwright.sync_api import expect
from src.POM_pages.base_page import BasePage
from src.POM_pages.personuppgifter_sida import Personuppgifter
from src.POM_pages.inkomstuppgifter_sida import Inkomstuppgifter
from src.POM_pages.laneuppgifter_sida import Laneuppgifter

def test_bil_full_loan_flow(shared_page):
    base = BasePage(shared_page)
    base.goto()
    base.assert_title_is_correct()
    base.bil_loan()

    pu = Personuppgifter(shared_page)
    data = pu.personuppgifter_form()
    expect(shared_page.get_by_role("textbox", name="Personnummer *")).to_have_value(data["pnr"])  # Kontrollera att personnumret är skattaverkets test personnummer.
    expect(shared_page.get_by_role("textbox", name="Förnamn")).to_have_value(data["first_name"])  # Kontrollera att förnamnet är fyllt med fake namn.
    expect(shared_page.get_by_role("textbox", name="Efternamn")).to_have_value(data["last_name"])  # Kontrollera att efternamnet är fyllt med fake efternamn.
    expect(shared_page.get_by_role("textbox", name="E-post")).to_have_value(data["email"])  # Kontrollera att e-posten är ifyllt med en fake e-post.
    expect(shared_page.get_by_role("textbox", name="Telefonnummer")).to_have_value(data["phone"])  # Kontrollera att telefonnumret är ifyllt med ett fake telefonnummer.
    expect(shared_page.get_by_role("textbox", name="Adress")).to_have_value(data["address"])  # Kontrollera att adressen är ifyllt med en fake adress.
    expect(shared_page.get_by_role("textbox", name="Postnummer")).to_have_value(data["postcode"])  # Kontrollera att postnumret är ifyllt med ett fake postnummer.
    expect(shared_page.get_by_role("textbox", name="Stad *")).to_have_value(data["city"])  # Kontrollera att orten är ifyllt med en fake ort.
    pu.submit_personuppgifter() 

    ip = Inkomstuppgifter(shared_page)
    income_data = ip.inkomstuppgifter_form()
    expect(shared_page.get_by_label("Månadsinkomst (SEK) *")).to_have_value(income_data["income"])
    expect(shared_page.get_by_role("textbox", name="Arbetsgivare *")).to_have_value(income_data["employer"])
    expect(shared_page.get_by_role("spinbutton", name="Sidoinkomst (SEK/månad)")).to_have_value(income_data["side_income"])
    ip.submit_inkomstuppgifter()

    invalid_loan_amounts = ["-1", "-50000", ""]

    for amount in invalid_loan_amounts:
        loan_amount_input = shared_page.get_by_role("spinbutton", name="Lånebelopp (SEK) *")
        loan_amount_input.fill(amount)
        shared_page.get_by_role("button", name="Nästa").click()
        expect(shared_page.get_by_text("Ange ett giltigt lånebelopp").first).to_be_visible()
        expect(loan_amount_input).to_be_visible()
    