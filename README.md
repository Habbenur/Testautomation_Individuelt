# Testautomation – Söderbröder Finans AB

Individuellt testautomationsprojekt för Söderbröder Finans AB (fiktivt scenario från FSH-kursen). Projektet innehåller automatiserade API-tester, GUI-tester och prestandatester (load test) för lånehanteringsflöden.

## Teknikstack

- **Python** + **pytest** – test runner
- **Playwright** – GUI-automatisering
- **requests** – API-tester
- **k6** – prestandatester (load test)
- **python-dotenv** – miljövariabler

## Projektstruktur

```
Testautomation_Individuelt/
├── src/
│   ├── POM_pages/       # Page Object Model för GUI-tester
│   └── helpers/         # Hjälpfunktioner
├── tests/
│   ├── api_tests/       # API-tester (partner loan m.m.)
│   └── ui_tests/        # GUI-tester för olika lånetyper
├── perf/
│   ├── lib/
│   └── tests/           # k6-baserade prestandatester
├── requirements.txt
└── pytest.ini
```

## Testöversikt

**API-tester** (`tests/api_tests/`):
- `test_api_helpers_partner_loan.py` – tester för partner-lånets API
- `test_demo.py` – demo/exempeltest

**GUI-tester** (`tests/ui_tests/`), ett flöde per lånetyp:
- Billån, båtlån, bröllopslån, renoveringslån, semesterlån
- Negativt test: ogiltigt lånebelopp

**Prestandatester** (`perf/tests/`):
- `partner_loan_flow.test.js` – lasttest för partnerlåneflödet med k6

## Installation

```bash
pip install -r requirements.txt
playwright install
```

Skapa en `.env`-fil i projektets rot med de miljövariabler som krävs för API- och prestandatesterna (t.ex. bas-URL och ev. testuppgifter).

## Köra testerna

**API- och GUI-tester** (körs från projektets rot):

```bash
pytest -s
```

**Prestandatester (k6)**:

```bash
set -a; source .env; set +a
k6 run perf/tests/partner_loan_flow.test.js
```
