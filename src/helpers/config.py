from dataclasses import dataclass, field
import os
from dotenv import load_dotenv
import faker
from src.helpers.skattaverket_testdata import SkatteverketTestdataClient, SkvResponse

faker = faker.Faker("sv_SE")  # Svensk lokal för fejkdata

load_dotenv()
@dataclass(frozen=True)
class Settings:
    base_url = "https://kzmcpfklrqymzazaxlmv.supabase.co/functions/v1" 
    api_key: str = os.getenv("X_API_KEY")
    admin_api_key: str = os.getenv("X_ADMIN_API_KEY")
    skv = SkatteverketTestdataClient()
    personal_number = skv.get_test_personnummer(limit=10)[0]
    first_name: str = faker.first_name()
    last_name: str = faker.last_name()
    email: str = faker.email()
    loan_amount: str = "100000"
    address: str = faker.address()
    postcode: str = faker.postcode()
    city: str = faker.city()
    phone: str = faker.phone_number()
    employment_type: str = "employed"
    employer: str = faker.company()
    income: str = "30000"
    repayment_months: str = "24"
    product_type: str = "personal"

settings = Settings()