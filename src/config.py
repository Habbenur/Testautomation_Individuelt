from dataclasses import dataclass, field
import os
from dotenv import load_dotenv
import faker
from src.api_helpers import BroderAPIHelper
from src.skattaverket_testdata import SkatteverketTestdataClient, SkvResponse

faker = faker.Faker("sv_SE")  # Svensk lokal för fejkdata

load_dotenv()
"""Fake svensk data för att skapa låneansökningar via API:et.
    Response Body:{
  "first_name": "string",        // Required
  "last_name": "string",         // Required
  "personal_number": "string",   // Required (ÅÅÅÅMMDDXXXX)
  "email": "string",             // Required
  "loan_amount": "string",       // Required (numeriskt)
  "address": "string",           // Optional
  "postcode": "string",          // Optional
  "city": "string",              // Optional
  "phone": "string",             // Optional
  "employment_type": "string",   // Optional (default: "employed")
  "employer": "string",          // Optional
  "income": "string",            // Optional (default: "30000")
  "repayment_months": "string",  // Optional (default: "12")
  "product_type": "string"       // Optional (default: "personal")
}"""
"""Response 200 OK
{
  "success": true,
  "application": {
    "id": "uuid",
    "reference_number": "PARTNER-XXXXXXXXX-XXXXXXX",
    "status": "approved",
    "first_name": "string",
    "last_name": "string",
    "loan_amount": "string",
    "created_at": "timestamp",
    ...
  },
  "message": "Application approved"
}"""
@dataclass(frozen=True)
class Settings:
    base_url = "https://kzmcpfklrqymzazaxlmv.supabase.co/functions/v1" 
    api_key: str = os.getenv("x-api-key")
    admin_api_key: str = os.getenv("x-admin-api-key")
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