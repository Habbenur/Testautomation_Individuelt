import pytest

def test_fill_loan_form(loan_page):
    loan_page.fill_loan_form(amount=100000, term=36)
    assert loan_page.page.get_by_text("Din låneansökan är mottagen").is_visible()
