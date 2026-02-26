import http from "k6/http";
import { check, fail } from "k6";

const SKV_DATASET_URL =
  "https://skatteverket.entryscape.net/rowstore/dataset/b4de7df7-63c0-4e7e-bb59-1f156a591763";

export function normalizePnrTo12Digits(pnr) {
  const digits = String(pnr).replace(/\D/g, "");
  if (digits.length !== 12) throw new Error(`Unexpected personnummer format: ${pnr}`);
  return digits;
}

export function getTestPersonnummer(limit = 10, offset = 0) {
  const res = http.get(`${SKV_DATASET_URL}?_limit=${limit}&_offset=${offset}`, {
    headers: { Accept: "application/json" },
    timeout: "10s",
    tags: { name: "SKV_get_personnummer" },
  });

  if (!check(res, { "SKV status 200": (r) => r.status === 200 })) {
    fail(`SKV fetch failed: status=${res.status} body=${res.body}`);
  }

  const json = res.json();
  const rows = (json && json.results) || [];
  const pnrs = rows.map((r) => r.testpersonnummer).filter(Boolean);
  if (pnrs.length === 0) fail("SKV dataset returned no testpersonnummer");
  return pnrs.map(normalizePnrTo12Digits);
}