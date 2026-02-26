import { randomItem, randomIntBetween, uuidv4 } from "https://jslib.k6.io/k6-utils/1.4.0/index.js";

const FIRST_NAMES = ["Erik", "Anna", "Johan", "Sara", "Linn", "Oskar", "Elin", "Karl", "Maja", "Nils"];
const LAST_NAMES = ["Andersson", "Johansson", "Karlsson", "Nilsson", "Eriksson", "Larsson", "Olsson", "Persson"];
const CITIES = ["Stockholm", "Göteborg", "Malmö", "Uppsala", "Västerås", "Örebro"];
const EMPLOYERS = ["Nordic AB", "SöderTech", "Svea Consulting", "Fjäll Systems", "Krona Group"];

function makeEmail() {
  return `k6.${uuidv4().slice(0, 8)}@example.test`;
}

function makeAddress() {
  return `Testgatan ${randomIntBetween(1, 180)}`;
}

function makePostcode() {
  return `${randomIntBetween(100, 999)} ${randomIntBetween(10, 99)}`;
}

export function buildLoanApplication(pnr12) {
  return {
    first_name: randomItem(FIRST_NAMES),
    last_name: randomItem(LAST_NAMES),
    personal_number: pnr12,
    email: makeEmail(),
    loan_amount: "100000",
    address: makeAddress(),
    postcode: makePostcode(),
    city: randomItem(CITIES),
    phone: `070${randomIntBetween(1000000, 9999999)}`,
    employment_type: "employed",
    employer: randomItem(EMPLOYERS),
    income: "30000",
    repayment_months: "24",
    product_type: "personal",
  };
}