import http from "k6/http";
import { BASE_URL, X_API_KEY, X_ADMIN_API_KEY } from "./config.js";

export function partnerHeaders() {
  return {
    "Content-Type": "application/json",
    Accept: "application/json",
    "x-api-key": X_API_KEY,
  };
}

export function adminHeaders() {
  return {
    "Content-Type": "application/json",
    Accept: "application/json",
    "x-admin-api-key": X_ADMIN_API_KEY,
  };
}

export function createLoanApplication(payload) {
  return http.post(`${BASE_URL}/partner-loan-api`, JSON.stringify(payload), {
    headers: partnerHeaders(),
    timeout: "30s",
    tags: { name: "POST_create" },
  });
}

export function listPartnerLoans() {
  return http.get(`${BASE_URL}/partner-loan-api`, {
    headers: { Accept: "application/json", "x-api-key": X_API_KEY },
    timeout: "30s",
    tags: { name: "GET_list" },
  });
}

export function updatePartnerLoan(referenceNumber, updateData) {
  const body = { reference_number: referenceNumber, ...updateData };
  return http.put(`${BASE_URL}/partner-loan-api`, JSON.stringify(body), {
    headers: adminHeaders(),
    timeout: "30s",
    tags: { name: "PUT_update" },
  });
}

export function deletePartnerLoan(referenceNumber) {
  return http.del(`${BASE_URL}/partner-loan-api?reference_number=${encodeURIComponent(referenceNumber)}`, null, {
    headers: { Accept: "application/json", "x-admin-api-key": X_ADMIN_API_KEY },
    timeout: "30s",
    tags: { name: "DEL_delete" },
  });
}