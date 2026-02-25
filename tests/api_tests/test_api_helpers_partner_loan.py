from src.api_client import BroderAPIClient, ApiResponse
from src.helpers.config import settings
from src.skattaverket_testdata import SkatteverketTestdataClient
import pytest
from faker import Faker
import re

fake = Faker("sv_SE")

def normalize_pnr_yyyymmddxxxx(pnr: str) -> str:
    digits = re.sub(r"\D", "", pnr)
    if len(digits) == 12:
        return digits
    raise ValueError(f"Unexpected personnummer format: {pnr}")

@pytest.fixture
def api_client() -> BroderAPIClient:
    return BroderAPIClient(
        base_url=settings.base_url,
        api_key=settings.api_key,
        admin_api_key=settings.admin_api_key
    )

def test_create_loan_application(api_client: BroderAPIClient):
    skv = SkatteverketTestdataClient()
    raw_pnr = skv.get_test_personnummer(limit=1)[0]
    personal_number = normalize_pnr_yyyymmddxxxx(raw_pnr)

    loan_data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "personal_number": personal_number,          # 12 digit, dash removed format
        "email": fake.email(),
        "loan_amount": str(settings.loan_amount),    # string numeriskt format
        "address": settings.address,
        "postcode": settings.postcode,
        "city": settings.city,
        "phone": settings.phone,
        "employment_type": settings.employment_type,
        "employer": settings.employer,
        "income": str(settings.income),
        "repayment_months": str(settings.repayment_months),
        "product_type": settings.product_type
    }

    resp = api_client.create_loan_application(loan_data)

    # HTTP status code
    assert resp.status_code == 200

    # Body content
    assert resp.json.get("success") is True
    msg = resp.json.get("message", "")
    assert msg.startswith("Application approved")

    app = resp.json.get("application")
    assert isinstance(app, dict)

    # Unika identifierare och status
    assert isinstance(app.get("id"), str) and len(app["id"]) > 10
    assert isinstance(app.get("reference_number"), str) and app["reference_number"].startswith("PARTNER-")
    assert app.get("status") == "approved"

    # Verifiera att det som skickades in i API:et matchar det som returnerades i svaret
    assert app.get("first_name") == loan_data["first_name"]
    assert app.get("last_name") == loan_data["last_name"]
    assert app.get("loan_amount") == loan_data["loan_amount"]


def test_get_partner_loans(api_client: BroderAPIClient):
    resp = api_client.get_partner_loans()

    assert resp.status_code == 200
    assert resp.json.get("success") is True
    assert isinstance(resp.json.get("loans"), list)

def test_update_partner_loan(api_client: BroderAPIClient):
    # Först, hämta en lista över lån för att få en giltig reference_number
    loans_resp = api_client.get_partner_loans()
    assert loans_resp.status_code == 200
    loans = loans_resp.json.get("loans", [])
    if not loans:
        pytest.skip("No partner loans available to update.")

    reference_number = loans[0].get("reference_number")
    assert reference_number, "Selected loan does not have a reference_number."

    update_data = {
        "reference_number": reference_number,
        "status": "denied",  # Exempel på uppdatering av status
        "loan_amount": "150000"  # Exempel på uppdatering av lånebelopp
    }

    update_resp = api_client.update_partner_loan(reference_number, update_data)

    assert update_resp.status_code == 200
    assert update_resp.json.get("success") is True
    updated_loan = update_resp.json.get("loan")
    assert updated_loan is not None
    assert updated_loan.get("reference_number") == reference_number
    assert updated_loan.get("status") == "denied"
    assert updated_loan.get("loan_amount") == "150000"
    assert update_resp.json.get("message") == "Loan updated successfully"

def test_delete_partner_loan(api_client: BroderAPIClient):
    # Först, hämta en lista över lån för att få en giltig reference_number
    loans_resp = api_client.get_partner_loans()
    assert loans_resp.status_code == 200
    loans = loans_resp.json.get("loans", [])
    if not loans:
        pytest.skip("No partner loans available to delete.")

    reference_number = loans[0].get("reference_number")
    assert reference_number, "Selected loan does not have a reference_number."

    delete_resp = api_client.delete_partner_loan(reference_number)
    assert delete_resp.status_code == 200
    assert delete_resp.json.get("success") is True
    assert delete_resp.json.get("reference_number") == reference_number
    assert delete_resp.json.get("message") == "Loan deleted successfully"

 