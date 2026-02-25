from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import requests

SKV_DATASET_URL = "https://skatteverket.entryscape.net/rowstore/dataset/b4de7df7-63c0-4e7e-bb59-1f156a591763"

@dataclass
class SkvResponse:
    status_code: int
    headers: dict[str, str]
    json: dict[str, Any]

class SkatteverketTestdataClient:
    def __init__(self, base_url: str = SKV_DATASET_URL, timeout_s: float = 10.0):
        self.base_url = base_url
        self.timeout_s = timeout_s
        self.session = requests.Session()

    def get_test_personnummer(self, *, limit: int = 10, offset: int = 0) -> list[str]:
        params = {"_limit": limit, "_offset": offset}

        r = self.session.get(
            self.base_url,
            params=params,
            headers={"Accept": "application/json"},
            timeout=self.timeout_s,
        )

        r.raise_for_status()

        payload = r.json()
        results = payload.get("results", [])

        return [
            row["testpersonnummer"]
            for row in results
            if row.get("testpersonnummer")
        ]