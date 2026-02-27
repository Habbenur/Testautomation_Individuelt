# Testautomation_Individuelt

# Köra Api och Gui tester kör kommandon i projektets root map
pytest -s

# Köra performance tester kör kommandon i projektets root map
set -a; source .env; set +a 
k6 run perf/tests/partner_loan_flow.test.js
 