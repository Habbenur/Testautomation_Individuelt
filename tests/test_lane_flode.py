import pytest
import re

from playwright.sync_api import expect

def test_base_page(base_sida):
    base_sida.goto()
    h1 = base_sida.page.locator("h1")
    expect(h1).to_have_text("Söderbröder Finans AB")
    expect(h1).to_be_visible()

def test_personuppgifter_page(personuppgifter_page):
    pu = personuppgifter_page
    
    data = pu.personuppgifter_form()

    expect(pu.page.get_by_role("textbox", name="Förnamn *")).to_have_value(data["first_name"])
    expect(pu.page.get_by_role("textbox", name="Efternamn *")).to_have_value(data["last_name"])
    expect(pu.page.get_by_role("textbox", name="E-post *")).to_have_value(data["email"])

def test_inkomstuppgifter_page(inkomstuppgifter_page):
    ip = inkomstuppgifter_page
    data = ip.inkomstuppgifter_form()

    expect(ip.page.get_by_label("Månadsinkomst (SEK) *")).to_have_value(data["income"])


def test_laneuppgifter_page(laneuppgifter_page):
    lp = laneuppgifter_page
    amount = 500000
    lp.laneuppgifter_form(amount=amount)

    expect(lp.page.get_by_role("spinbutton", name="Lånebelopp (SEK) *")).to_have_value(str(amount))
    expect(lp.page.get_by_role("heading", name="Din månadskostnad:")).to_be_visible()
    
    lp.submit_laneuppgifter()
    expect(lp.page.get_by_text("Din låneansökan är mottagen")).to_be_visible()


    

    