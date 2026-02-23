from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from urllib import response
import requests

@dataclass(frozen=True)
class ApiResponse:
    status_code: int
    headers: dict[str, str]
    json: dict[str, Any]
    text: str

class BroderAPIHelper:
    """Helper functions for SöderBröder API"""
    def __init__(self, base_url: str, api_key: str, admin_api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.admin_api_key = admin_api_key

    def create_loan_application(self, data: dict[str, Any]) -> ApiResponse:
        url = f"{self.base_url}/partner-loan-api"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,      # API key for authentication
            "Accept": "application/json",
        }

        r = requests.post(url, json=data, headers=headers)

        # Debug output for non-OK responses
        if not r.ok:
            print("STATUS:", r.status_code)
            print("BODY:", r.text)

        # JSON parsing with error handling
        try:
            payload = r.json()
        except ValueError:
            payload = {}

        r.raise_for_status()

        return ApiResponse(
            status_code=r.status_code,
            headers=dict(r.headers),
            json=payload,
            text=r.text,
        )

    def get_partner_loans(self) -> ApiResponse:
        url = f"{self.base_url}/partner-loan-api"
        headers = {
            "x-api-key": self.api_key,
            "Accept": "application/json",
        }

        r = requests.get(url, headers=headers)

        # Debug output for non-OK responses
        if not r.ok:
            print("STATUS:", r.status_code)
            print("BODY:", r.text)

        # JSON parsing with error handling
        try:
            payload = r.json()
        except ValueError:
            payload = {}

        r.raise_for_status()

        return ApiResponse(
            status_code=r.status_code,
            headers=dict(r.headers),
            json=payload,
            text=r.text,
        )
    def get_partner_loans_list(self):
        url = f"{self.base_url}/partner-loan-api"   
        headers = {
            "x-api-key": self.api_key,
            "Accept": "application/json",
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        print(f"Antal lån: {data['total_loans']}")
        print(f"Lån: {data['loans']}")

    def update_partner_loan(self, reference_number: str, update_data: dict[str, Any]) -> ApiResponse:
        url = f"{self.base_url}/partner-loan-api"
        headers = {
            "Content-Type": "application/json",
            "x-admin-api-key": self.admin_api_key,
            "Accept": "application/json",
        }
        payload = {"reference_number": reference_number}
        payload.update(update_data)

        r = requests.put(url, json=payload, headers=headers)

        # Debug output for non-OK responses
        if not r.ok:
            print("STATUS:", r.status_code)
            print("BODY:", r.text)

        # JSON parsing with error handling
        try:
            response_payload = r.json()
        except ValueError:
            response_payload = {}

        r.raise_for_status()

        return ApiResponse(
            status_code=r.status_code,
            headers=dict(r.headers),
            json=response_payload,
            text=r.text,
        )
