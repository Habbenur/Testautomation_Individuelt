from src.api_helpers import BroderAPIHelper
from src.config import settings
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
def api_helper() -> BroderAPIHelper:
    return BroderAPIHelper(
        base_url=settings.base_url,
        api_key=settings.api_key,
        admin_api_key=settings.admin_api_key
    )

def test_create_loan_application(api_helper: BroderAPIHelper):
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

    resp = api_helper.create_loan_application(loan_data)

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