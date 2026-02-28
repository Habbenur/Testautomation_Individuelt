# Test ramverk för Söderbröder Finans AB
I det här projektet, finns automatiserad API och GUI tester för Söderbröder Finans AB. Alltså finns Load test för API.

# För att köra Api och Gui tester, kör den kommandon i projektets root map:
pytest -s

# För att köra performance tester, kör den kommandon i projektets root map:
set -a; source .env; set +a 
k6 run perf/tests/partner_loan_flow.test.js
 