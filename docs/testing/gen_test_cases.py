#!/usr/bin/env python3
"""
Single source of truth for the PetStore EE7 test case catalogue.
Generates test-cases.md (human-readable, ISO/IEC/IEEE 29119-3 test case specification fields)
and test-cases.csv (import into Xray / TestRail / Excel).

Run: python3 docs/testing/gen_test_cases.py [--check]
"""
import csv, io, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS = ["id", "title", "level", "traces", "pre", "steps", "expected", "priority", "tool", "status", "current"]
# status: Existing (test class exists) | New (to be written)
# current: expected outcome on the as-built code: PASS | FAIL (defect id) | N/A

T = []
def tc(*a): T.append(dict(zip(FIELDS, a)))

# ---------------- Unit ----------------
tc("TC-UNIT-01","Entity equals/hashCode contracts","Unit","All entities","-","Run EqualsVerifier on Address, Category, Country, CreditCard, Customer, Item, OrderLine, Product, PurchaseOrder","Contracts hold (symmetry, consistency, non-nullity)","Low","JUnit + EqualsVerifier","Existing (*Test.java)","PASS")
tc("TC-UNIT-02","OrderLine and cart-line subtotal","Unit","UC11","Item unitCost=10.00","1. new OrderLine(2, item) 2. getSubTotal()","20.00 (use BigDecimal; Float may drift)","Medium","JUnit + AssertJ","New","PASS")
tc("TC-UNIT-03","Customer age calculation","Unit","UC09","dateOfBirth = today minus 30 years plus 1 day","calculateAge()","age = 29; null DOB gives null age","Low","JUnit","New","PASS")
tc("TC-UNIT-04","Password digest is not plain text","Unit","UC05; SEC-03","-","digestPassword('secret')","Result differs from input and is not reversible; target: PBKDF2 hash with a per-user salt, where two users with the same password get different hashes","High","JUnit","New","FAIL (SEC-03: same hash for same password)")
tc("TC-UNIT-05","Cart add increments quantity for same item","Unit","UC10","Transient conversation mocked","addItemToCart(itemId=1000) twice","One line, quantity 2; conversation.begin() called once","High","JUnit + Mockito","New","PASS")
tc("TC-UNIT-06","Cart remove last line","Unit","UC12","Cart with 1 line","removeItemFromCart(itemId)","Cart empty; shoppingCartIsEmpty() true","Medium","JUnit + Mockito","New","PASS")
tc("TC-UNIT-07","Cart total","Unit","UC11","Lines 2x10.00 and 1x12.00","getTotal()","32.00","High","JUnit","New","PASS")
tc("TC-UNIT-08","Order totals with VAT and discount","Unit","UC13; BUG-02","vat=20%, discount=5%, lines 32.00","Price the order","subtotal 32.00, discount 1.60, VAT 6.08, total 36.48","High","JUnit","New","FAIL (BUG-02: totals null)")
tc("TC-UNIT-09","Custom constraints @Email @Login @Price @NotEmpty","Unit","UC05, UC15","Bean Validation factory","Validate valid and invalid samples (e.g. email 'a@b', login > 10 chars, price 9.99)","Invalid samples produce exactly one violation each (@ReportAsSingleViolation)","Medium","JUnit + Hibernate Validator","New","PASS")

# ---------------- Integration ----------------
tc("TC-INT-01","Services deploy and CRUD entities","Integration","UC15-UC18","Arquillian WildFly profile","should_be_deployed; should_crud per service","Create/find/update/delete succeed; counts restored","Medium","Arquillian","Existing (*ServiceIT, 7 classes)","PASS")
tc("TC-INT-02","Admin beans CRUD and paginate","Integration","UC15-UC19","Arquillian","should_crud; should_paginate for 7 admin beans","Pages of 10; CRUD succeeds","Medium","Arquillian","Existing (view/admin/*BeanIT)","PASS")
tc("TC-INT-03","Entities persist with valid data and reject invalid","Integration","UC05, UC13","Arquillian + JPA","Persist valid Customer, PurchaseOrder; persist invalid (missing street1)","Valid rows stored; ConstraintViolationException for invalid","Medium","Arquillian","Existing (model/*IT)","PASS")
tc("TC-INT-04","createOrder with empty cart","Integration","UC13","Signed-in customer","PurchaseOrderService.createOrder(customer, card, [])","ValidationException; no row inserted; transaction rolled back","High","Arquillian","New","PASS")
tc("TC-INT-05","createOrder persists order, lines and orderDate","Integration","UC13","Seed items 1000, 1002","createOrder with 2 lines","1 purchase_order, 2 order_line rows; orderDate = today","High","Arquillian","New","PASS")
tc("TC-INT-06","Purchase order search by delivery city","Integration","UC18; BUG-01","Orders exist","PurchaseOrderBean.example.deliveryAddress.city='Black'; paginate()","Matching orders listed","Medium","Arquillian","New","FAIL (BUG-01: root.get('city') on PurchaseOrder)")
tc("TC-INT-07","Catalog search is case-insensitive","Integration","UC02","Seed data","CatalogService.searchItems('fIsH')","Items of the Fish category returned","Medium","Arquillian","New","PASS")
tc("TC-INT-08","Data survives restart","Integration","OPS-01; QS-5","PostgreSQL via Testcontainers","Create customer; redeploy WAR; find customer","Customer still present","Medium","Arquillian + Testcontainers","New","FAIL (OPS-01: drop-and-create)")

# ---------------- API ----------------
tc("TC-API-01","Resources respond in JSON and XML","API","UC21","Deployed WAR","GET /rest/categories with Accept JSON, then XML","200 for both","Low","Arquillian REST client","Existing (*EndpointIT)","PASS")
tc("TC-API-02","Create returns 201 and Location","API","UC21","-","POST /rest/categories {name, description}","201; Location /rest/categories/{id}; GET on Location returns 200","Medium","REST Assured","New","PASS")
tc("TC-API-03","Unknown id returns 404","API","UC21","-","GET /rest/items/999999","404","Low","REST Assured","New","PASS")
tc("TC-API-04","Stale version returns conflict","API","UC21","Category v1 exists","PUT twice with the same version","Second PUT returns 409 (v1 contract) / 412 (v1 target)","Medium","REST Assured","New","PASS")
tc("TC-API-05","Invalid body returns problem details","API","UC21; A5","-","POST /rest/categories {name: ''}","400/422 with application/problem+json","Medium","REST Assured","New","FAIL (A5: 500 / non-JSON error)")
tc("TC-API-06","Responses conform to OpenAPI contract","API","ADR-0005","openapi-v1.yaml","Schemathesis run against /api/v1","No schema violations, no 5xx","High","Schemathesis","New","N/A (v1 not implemented)")
tc("TC-API-07","Pagination is bounded","API","UC21; A6; OWASP API4","-","GET /rest/items?max=1000000","Server caps page size (<= 100)","Medium","REST Assured","New","FAIL (A6: unbounded)")

# ---------------- E2E ----------------
tc("TC-E2E-01","Browse category to item","E2E","UC01, UC03","Anonymous","1. Open /shopping/main.xhtml 2. Click Fish 3. Click Angelfish 4. Click Large","Item page shows name, price 10.00 $, description; no Add to cart","High","Playwright","New","PASS")
tc("TC-E2E-02","Keyword search","E2E","UC02","Anonymous","Enter 'koi' in navbar search; press Search","Results list Koi items with category/product and price","High","Playwright","New","PASS")
tc("TC-E2E-03","Register a new customer","E2E","UC05, UC06","Unique login","1. Sign on > New customer with matching passwords 2. Fill required details 3. Submit","Redirect to main; navbar shows Welcome <first name>","High","Playwright","New","PASS")
tc("TC-E2E-04","Registration rejects mismatched passwords","E2E","UC05","-","New customer with password != password2","Warning 'both_pwd_same'; stays on sign on","Medium","Playwright","New","PASS")
tc("TC-E2E-05","Sign in with valid credentials","E2E","UC07","Seed user 'user'","Login user / user","Signed in; Welcome User","High","Playwright","New","PASS")
tc("TC-E2E-06","Sign in with wrong password is rejected","E2E","UC07; SEC-01; QS-1","Seed user 'user'","Login user / wrong-password","Error message; not signed in","Critical","Playwright","New","FAIL (SEC-01)")
tc("TC-E2E-07","Add to cart, change quantity, remove","E2E","UC10, UC11, UC12","Signed in","1. Add Large twice 2. Open cart 3. Set qty 3, Update 4. Remove","Quantity shows 2 then 3; total updates; removal empties cart","High","Playwright","New","FAIL (UX-06: Update is a no-op)")
tc("TC-E2E-08","Checkout places order","E2E","UC13, UC14","Signed in, cart 2 lines","Check Out; enter card 4111111111111111 VISA 12/28; Submit","Order confirmed page lists lines, order number and total","Critical","Playwright","New","FAIL (BUG-02/UX-05: no total/number)")
tc("TC-E2E-09","Delivery address edit does not change account","E2E","UC13, UC09; UX-04","Signed in","Edit city on confirm order; submit; open Account","Account address unchanged","Medium","Playwright","New","FAIL (UX-04)")
tc("TC-E2E-10","Sign out ends cart and session","E2E","UC08; SEC-07","Signed in with cart","Log out; press browser Back; reload cart URL","Signed out message; cart empty; protected pages redirect to sign on","High","Playwright","New","FAIL (SEC-07 / SEC-02)")
tc("TC-E2E-11","Switch language to French","E2E","UC04","-","Languages > Français","Labels rendered in French; html lang='fr'","Low","Playwright","New","FAIL (UX-09: no lang attribute)")
tc("TC-E2E-12","Admin creates an item","E2E","UC15","Administrator signed in (target)","Admin > Item > Create New; fill; Save","Item appears in search and in storefront","Medium","Playwright","New","PASS")

# ---------------- Accessibility ----------------
tc("TC-A11Y-01","Automated WCAG 2.2 AA scan of all storefront views","Accessibility","WCAG 2.2 AA","Seeded data","Run axe-core on WF-01..WF-11 (signed out and signed in)","Zero serious/critical violations","High","Playwright + axe-core","New","FAIL (UX-02, UX-07, UX-09)")
tc("TC-A11Y-02","Keyboard-only checkout","Accessibility","WCAG 2.1.1, 2.4.7; QS-7","Signed in","Complete TC-E2E-08 with keyboard only","Completes; visible focus on every control","High","Manual + Playwright keyboard API","New","N/A (to be measured)")
tc("TC-A11Y-03","Reflow at 320 px","Accessibility","WCAG 1.4.10; UX-08","-","Viewport 320x640, zoom 400% on home and checkout","No horizontal scrolling; categories reachable","Medium","Playwright","New","FAIL (UX-08 image map)")

# ---------------- Security (OWASP WSTG v4.2 / ASVS 5.0) ----------------
tc("TC-SEC-01","Authentication bypass: any password accepted","Security","WSTG-ATHN-04; ASVS V6; SEC-01","Seed user 'admin'","POST sign-in with login=admin, password=x","Rejected; failure logged; lockout after 5 attempts","Critical","ZAP script / Playwright","New","FAIL (SEC-01)")
tc("TC-SEC-02","Forced browsing to admin","Security","WSTG-ATHZ-02; SEC-02","Anonymous","GET /applicationPetstore/admin/customer/search.xhtml","302 to login or 403","Critical","ZAP / curl","New","FAIL (SEC-02)")
tc("TC-SEC-03","Unauthenticated REST write","Security","WSTG-ATHZ-02; OWASP API2/API5; SEC-02","Anonymous","DELETE /rest/categories/1000","401","Critical","REST Assured","New","FAIL (SEC-02)")
tc("TC-SEC-04","Excessive data exposure: password hash","Security","OWASP API3:2023; SEC-04","Anonymous","GET /rest/customers","No 'password' property in any response","High","REST Assured","New","FAIL (SEC-04)")
tc("TC-SEC-05","Default credentials disclosure","Security","WSTG-ATHN-02; SEC-08","Anonymous","Open sign on page; try admin/admin","No credential hint rendered; default accounts disabled in production","High","Playwright","New","FAIL (SEC-08)")
tc("TC-SEC-06","Session fixation","Security","WSTG-SESS-03; ASVS V7","Capture JSESSIONID before sign-in","Sign in; compare session id","Session id changes after authentication","High","ZAP / Playwright","New","FAIL (expected: id not rotated)")
tc("TC-SEC-07","Session termination at logout","Security","WSTG-SESS-06; SEC-07","Signed in","Log out; replay old JSESSIONID","Old session invalid","High","ZAP","New","FAIL (SEC-07)")
tc("TC-SEC-08","Reflected XSS in search","Security","WSTG-INPV-01","-","Search for <script>alert(1)</script> and \" onmouseover=alert(1)","Payload rendered escaped (Facelets escapes by default)","High","ZAP active scan","New","PASS (expected)")
tc("TC-SEC-09","SQL/JPQL injection in search","Security","WSTG-INPV-05","-","Search for ' OR '1'='1 and %_ wildcards","No error; only literal matches (named parameters used)","High","ZAP / sqlmap","New","PASS (expected)")
tc("TC-SEC-10","CSRF on state-changing actions","Security","WSTG-SESS-05","Signed in","Replay confirmOrder POST from another origin without ViewState","Rejected (javax.faces.ViewState / protected views)","High","ZAP / manual","New","N/A (to be measured)")
tc("TC-SEC-11","Security headers and TLS","Security","WSTG-CONF-07, CONF-12; ASVS V3","Deployed behind edge","Inspect response headers","HSTS, CSP, X-Content-Type-Options, frame-ancestors, Referrer-Policy present; TLS 1.2+ only","High","ZAP baseline","New","FAIL (no headers/TLS configured)")
tc("TC-SEC-12","Card data at rest","Security","PCI DSS v4.0.1 Req. 3; SEC-05","Order placed","Query purchase_order.credit_card_number","No PAN stored (token + last 4 only)","Critical","SQL assertion in IT","New","FAIL (SEC-05)")
tc("TC-SEC-13","Brute-force protection","Security","WSTG-ATHN-03","-","25 wrong passwords in 1 minute","Throttled / locked; alert raised","High","ZAP / k6","New","FAIL (no lockout)")
tc("TC-SEC-14","Information disclosure via debug page and footer","Security","UC20; WSTG-INFO-05; UX-12","Anonymous","GET /debug.xhtml; view footer","Not reachable in production; no conversation id shown","Medium","curl","New","FAIL")
tc("TC-SEC-15","Vulnerable components","Security","OWASP A06:2021; DEP-01","Build","OWASP Dependency-Check on WAR incl. WebJars","No dependency with CVSS >= 7.0","High","dependency-check-maven","New","FAIL (expected: jQuery 2.2.4, Bootstrap 3.3.7)")
tc("TC-SEC-16","Secrets in repository","Security","ASVS V13","-","gitleaks on full history","No secrets","High","gitleaks","New","PASS (expected)")

# ---------------- Governance / policy as code ----------------
tc("TC-GOV-01","Layered architecture rules","Governance","ARCH-01, ARCH-02; QS-6","-","ArchUnit layeredArchitecture() and slices().should().beFreeOfCycles()","All rules pass","Medium","ArchUnit","New","FAIL (ARCH-01/02)")
tc("TC-GOV-02","Licence allow-list","Governance","Licensing","-","license-maven-plugin aggregate-add-third-party; compare to allow-list (Apache-2.0, MIT, BSD, EPL-2.0, LGPL)","No disallowed licence; THIRD-PARTY report produced","Medium","license-maven-plugin","New","N/A (to be measured)")
tc("TC-GOV-03","SBOM generated and attached","Governance","Supply chain (SLSA)","-","cyclonedx-maven-plugin makeAggregateBom","bom.json produced and attached to release","Medium","CycloneDX","New","FAIL (not configured)")
tc("TC-GOV-04","Container policy","Governance","Policy as code","Dockerfile/K8s manifests (target)","conftest test with Rego: non-root, read-only FS, no :latest, resources set","All policies pass","Medium","conftest / OPA","New","N/A (target)")
tc("TC-GOV-05","Docs in sync with code","Governance","Docs-as-code","-","docs/render.sh --check","Diagrams valid, headings per Annex A, references resolved, pages fresh","Medium","render.sh","New","PASS")
tc("TC-GOV-06","Coverage gate","Governance","Test strategy","-","mvn verify with JaCoCo check rule","line >= 80%, branch >= 70%","Medium","JaCoCo","New","FAIL (no JaCoCo)")

# ---------------- Audit ----------------
tc("TC-AUD-01","Security events are logged","Audit","ASVS V16 (logging); SEC-01","-","Sign in success/failure, logout, admin CRUD, order placement","Each event logged once with timestamp, user, source IP, outcome; no passwords or PANs in logs","High","Log assertion in IT","New","FAIL (only method entry/exit logged)")
tc("TC-AUD-02","Release evidence archived","Audit","Release process","Tagged release","Collect test, coverage, SBOM, ZAP reports","Artifacts attached to the GitHub release","Low","GitHub Actions","New","N/A (target)")

# ---------------- Performance ----------------
tc("TC-PERF-01","Catalogue browse load","Performance","QS-4","PostgreSQL, 2nd-level cache on","Gatling 50 virtual users, 10 min, browse scenario","p95 < 300 ms, errors < 1%","Medium","Gatling","New","N/A (to be measured)")
tc("TC-PERF-02","Checkout throughput","Performance","QS-4","-","10 checkouts/min for 30 min","p95 < 800 ms; no DB deadlocks","Medium","Gatling","New","N/A (to be measured)")


def md() -> str:
    lv = {}
    for t in T:
        lv.setdefault(t["level"], []).append(t)
    fails = sum(1 for t in T if t["current"].startswith("FAIL"))
    passes = sum(1 for t in T if t["current"].startswith("PASS"))
    out = ["<!-- GENERATED by docs/testing/gen_test_cases.py. Edit the generator, not this file. -->",
           "# PetStore EE7 — Test Case Catalogue", "",
           "Fields follow the **ISO/IEC/IEEE 29119-3:2021** test case specification: identifier, objective, priority,",
           "traceability, preconditions, input/steps, expected result. Security cases reference **OWASP WSTG v4.2** and",
           "**ASVS 5.0**; accessibility cases reference **WCAG 2.2**. A CSV copy for test-management tools is in",
           "[`test-cases.csv`](test-cases.csv).", "",
           f"**Summary:** {len(T)} test cases. Expected result on the as-built code: {passes} PASS, {fails} FAIL (known defects),",
           f"{len(T)-passes-fails} not yet measurable. Existing automated tests cover {sum(1 for t in T if t['status'].startswith('Existing'))} of these cases.", "",
           "| Level | Count |", "|---|---|"]
    for k, v in lv.items():
        out.append(f"| {k} | {len(v)} |")
    out.append("")
    for k, v in lv.items():
        out += [f"## {k}", "", "| ID | Title | Traces | Preconditions | Steps | Expected result | Priority | Tool | Status | Expected on current build |", "|---|---|---|---|---|---|---|---|---|---|"]
        for t in v:
            cells = [t[f].replace("|", "\\|") for f in ["id","title","traces","pre","steps","expected","priority","tool","status","current"]]
            if t["current"].startswith("FAIL"):
                cells[-1] = f"**{cells[-1]}**"
            out.append("| " + " | ".join(cells) + " |")
        out.append("")
    # traceability matrix: use case -> test cases
    out += ["## Traceability: use case to test cases", "", "| Use case | Test cases |", "|---|---|"]
    ucs = {}
    import re
    for t in T:
        for m in re.findall(r"UC(\d{2})(?:-UC(\d{2}))?", t["traces"]):
            a = int(m[0]); b = int(m[1]) if m[1] else a
            for n in range(a, b + 1):
                ucs.setdefault(n, []).append(t["id"])
    for n in range(1, 22):
        out.append(f"| UC{n:02d} | {', '.join(ucs.get(n, [])) or '**none (gap)**'} |")
    out.append("")
    return "\n".join(out)


def csvtext() -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=FIELDS, lineterminator="\n")
    w.writeheader()
    w.writerows(T)
    return buf.getvalue()


def main():
    files = {ROOT / "test-cases.md": md(), ROOT / "test-cases.csv": csvtext()}
    ids = [t["id"] for t in T]
    assert len(ids) == len(set(ids)), "duplicate test case id"
    if "--check" in sys.argv:
        stale = [p for p, c in files.items() if not p.exists() or p.read_text() != c]
        for p in stale:
            print(f"stale: {p.name}")
        sys.exit(1 if stale else 0)
    for p, c in files.items():
        p.write_text(c)
    print(f"Wrote {len(T)} test cases")


if __name__ == "__main__":
    main()
