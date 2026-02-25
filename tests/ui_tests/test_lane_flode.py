from playwright.sync_api import expect
from src.POM_pages.base_page import BasePage
from src.POM_pages.personuppgifter_sida import Personuppgifter
from src.POM_pages.inkomstuppgifter_sida import Inkomstuppgifter
from src.POM_pages.laneuppgifter_sida import Laneuppgifter

def test_full_loan_flow(shared_page):
    base = BasePage(shared_page)
    base.goto()
    base.assert_title_is_correct()
    """
    Välj en lånetyp och gå vidare till personuppgifter-sidan
    tex: 
    base.bil_loan() eller 
    base.boat_loan() eller 
    base.brollop_loan() eller 
    base.renoverings_loan() eller 
    base.semester_loan()
    """
    base.boat_loan()  # eller bil_loan, brollop_loan, renoverings_loan, semester_loan

    pu = Personuppgifter(shared_page)
    data = pu.personuppgifter_form()
    expect(shared_page.get_by_role("textbox", name="Personnummer *")).to_have_value(data["pnr"])  # Kontrollera att personnumret är ifyllt
    expect(shared_page.get_by_role("textbox", name="Förnamn")).to_have_value(data["first_name"])  # Kontrollera att förnamnet är ifyllt
    pu.submit_personuppgifter() 

    ip = Inkomstuppgifter(shared_page)
    ip.inkomstuppgifter_form()
    ip.submit_inkomstuppgifter()

    lp = Laneuppgifter(shared_page)
    lp.laneuppgifter_form(amount=500000)
    lp.submit_laneuppgifter()

    expect(shared_page.get_by_text("Din låneansökan är mottagen")).to_be_visible()