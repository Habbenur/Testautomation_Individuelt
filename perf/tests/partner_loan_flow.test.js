import { check, group, sleep, fail } from "k6";
import { randomItem, randomIntBetween } from "https://jslib.k6.io/k6-utils/1.4.0/index.js";

import { assertConfig } from "../lib/config.js";
import { getTestPersonnummer } from "../lib/skv_client.js";
import { buildLoanApplication } from "../lib/data_factory.js";
import { createLoanApplication, listPartnerLoans, updatePartnerLoan, deletePartnerLoan } from "../lib/broder_client.js";

export const options = {
  thresholds: {
    // Global
    http_req_failed: ["rate<0.01"],         // <1% error
    http_req_duration: ["p(95)<900"],       // global p95
    checks: ["rate>0.98"],                  // check pass rate

    // Endpoint bazlı (tags.name)
    "http_req_duration{name:POST_create}": ["p(95)<1200"],
    "http_req_duration{name:GET_list}": ["p(95)<600"],
    "http_req_duration{name:PUT_update}": ["p(95)<1200"],
    "http_req_duration{name:DEL_delete}": ["p(95)<1200"],
  },
  scenarios: {
    partnerLoanFlow: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "30s", target: 5 },
        { duration: "1m", target: 20 },
        { duration: "30s", target: 0 },
      ],
      gracefulRampDown: "10s",
    },
  },
};

export function setup() {
  assertConfig();
  const pnrPool = getTestPersonnummer(10, 0);
  return { pnrPool };
}

export default function (data) {
  const pnr12 = randomItem(data.pnrPool);
  const appPayload = buildLoanApplication(pnr12);

  let referenceNumber = null;

  group("create", () => {
    const res = createLoanApplication(appPayload);
    const ok = check(res, {
      "create status 200": (r) => r.status === 200,
      "create success true": (r) => r.json("success") === true,
      "create message approved": (r) => {
        const msg = r.json("message");
        return typeof msg === "string" && msg.startsWith("Application approved");
      },
      "create has reference_number": (r) => {
        const rn = r.json("application.reference_number");
        return typeof rn === "string" && rn.startsWith("PARTNER-");
      },
    });

    if (!ok) fail(`Create failed: status=${res.status} body=${res.body}`);
    referenceNumber = res.json("application.reference_number");
  });

  group("list", () => {
    const res = listPartnerLoans();
    check(res, {
      "list status 200": (r) => r.status === 200,
      "list success true": (r) => r.json("success") === true,
      "list loans array": (r) => Array.isArray(r.json("loans")),
    });
  });

  group("update", () => {
    const res = updatePartnerLoan(referenceNumber, { status: "denied", loan_amount: "150000" });
    check(res, {
      "update status 200": (r) => r.status === 200,
      "update success true": (r) => r.json("success") === true,
      "update message ok": (r) => r.json("message") === "Loan updated successfully",
      "update ref matches": (r) => r.json("loan.reference_number") === referenceNumber,
      "update status denied": (r) => r.json("loan.status") === "denied",
      "update loan_amount 150000": (r) => String(r.json("loan.loan_amount")) === "150000",
    });
  });

  group("delete", () => {
    const res = deletePartnerLoan(referenceNumber);
    check(res, {
      "delete status 200": (r) => r.status === 200,
      "delete success true": (r) => r.json("success") === true,
      "delete ref matches": (r) => r.json("reference_number") === referenceNumber,
      "delete message ok": (r) => r.json("message") === "Loan deleted successfully",
    });
  });

  sleep(randomIntBetween(1, 3));
}