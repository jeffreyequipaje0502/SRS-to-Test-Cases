---
inclusion: auto
name: srs-to-testcases
description: Activated when the user asks to generate test cases, create test scenarios, or analyze an SRS or requirements document. Provides the full workflow for producing an Azure DevOps-importable .xlsx file from a PDF SRS.
---

# Skill: SRS to Test Cases Generator

## CIB 2.0 Application UI Reference

This skill automatically loads the verified CIB 2.0 UI reference captured from the live QA environment.
Use the labels, navigation paths, field names, and button names from this reference in ALL test case steps.

#[[file:../steering/cib-app-ui-reference.md]]

---

## Purpose
You are a senior QA Automation Engineer. When this skill is activated, your job is to:
1. Read and deeply analyze a Software Requirements Specification (SRS) document (PDF) provided by the user
2. Extract every discrete acceptance criterion into a numbered checklist
3. Generate comprehensive, production-ready test cases that cover EVERY item on that checklist
4. Verify coverage — every checklist item must map to at least one test case
5. Output a ready-to-import Excel file (.xlsx) in Azure DevOps format
6. Provide a plain-language chat summary of what was covered

---

## How to Activate
The user will provide an SRS document using `#File` in chat, or by dragging a PDF into the chat window.
They may say something like: *"Generate test cases from this SRS"* or *"Create test scenarios for this document."*

**Important — large PDFs:** If the user drags a large PDF (10+ pages) directly into chat, the API may reject the request with a deserialization error because the inlined page content creates a JSON body too large to parse. If this happens, instruct the user to convert the PDF to text first:

```
python scripts/pdf_to_text.py "path/to/SRS.pdf"
```

This creates a `.txt` file the user can reference with `#File` instead. Text is dramatically smaller than base64-encoded page images and avoids the error.

---

## Step 1: SRS Analysis

When analyzing the SRS, extract and categorize the following:

### What to look for:
- **Feature/Module Name** — what system or feature the document describes
- **Functional Requirements** — every requirement ID and its description
- **Business Rules** — rules that govern behavior (limits, validations, conditions)
- **User Flows / Process Flows** — step-by-step sequences a user goes through
- **Input Fields and Validations** — field constraints, formats, mandatory/optional
- **Error Messages and Handling** — what happens when something goes wrong
- **Integration Points** — APIs, third-party systems, backend services
- **Security and Authentication Requirements** — login, session, authorization
- **Edge Cases mentioned** — boundary values, special conditions
- **Non-functional hints** — performance, timeout behavior, UI display rules

### Analysis output (internal, used to generate test cases):
For each identified requirement or flow, mentally note:
- What is the happy path?
- What can go wrong? (negative scenarios)
- What are the boundaries? (min/max values, empty fields, special characters)
- Are there role-based or permission-based variations?
- What integrations need to be verified end-to-end?

---

## Step 2: Requirements Extraction Checklist (MANDATORY)

**Before writing a single test case**, you MUST build a numbered Requirements Checklist by reading the SRS section by section.

### How to build the checklist:
- Go through every section of the SRS sequentially
- For EACH numbered item, bullet point, "shall" statement, status value, field name, validation rule, error message, or UI behavior described — create one checklist entry
- Number them sequentially: REQ-001, REQ-002, REQ-003 ...
- Group them by feature/section for clarity

### Example checklist format:
```
SECTION 2.1 – Transaction History Piecemeal
REQ-001: Transaction History view displays status: Success
REQ-002: Transaction History view displays status: Failed
REQ-003: Transaction History view displays status: Sent for Processing
REQ-004: Transaction History view displays status: Queued for Processing
REQ-005: Transaction History view displays status: Approved
REQ-006: Transaction History view displays Processing Date (equivalent to value date)
REQ-007: Success/Failed status displayed when manually updated via iCare Ticket or Service Request
REQ-008: Covers Own Account Fund Transfer (PHP, USD)
REQ-009: Covers Third Party Transfer (PHP, USD)
REQ-010: Covers Instapay
... and so on for EVERY stated requirement
```

### Rules:
- Do NOT skip any requirement because it seems minor or obvious
- Each distinct status value is its own checklist entry
- Each distinct transaction type is its own checklist entry
- Each mandatory/optional field distinction is its own checklist entry
- Each error message or validation behavior is its own checklist entry
- Each UI element behavior (radio button, checkbox, auto-populate) is its own checklist entry

This checklist is your **source of truth** for coverage. You cannot claim coverage is complete unless every REQ-XXX has at least one test case mapped to it.

---

## Step 3: Test Case Generation Strategy

Generate test cases across these categories for every feature/flow found.
**Use the Requirements Checklist from Step 2 as your guide — do not move on until every REQ is covered.**

### 1. Positive / Happy Path Tests
- Normal flow with valid data
- All mandatory fields filled correctly
- Successful completion of the main user journey
- **Each distinct status value must have its own test case** (do not combine statuses into one test)
- **Each distinct transaction type must have at least one test case** — and each transaction type that also varies by currency (PHP vs USD) must have separate test cases for each currency
- **Download / action button availability must be tested per status** — if a button (e.g., Download Fund Transfer Advice) should be available regardless of status, write separate tests for each status value to confirm the button is present and enabled

### 2. Negative / Error Handling Tests
- Invalid input data (wrong format, out-of-range values)
- Missing mandatory fields
- Unauthorized access attempts
- Expired sessions or tokens
- System/network error responses
- **Each mandatory field must have a negative test for when it is missing**

### 3. Boundary / Edge Case Tests
- Minimum and maximum allowed values
- Zero values, empty strings, null inputs
- Maximum character limits on text fields
- Special characters in input fields
- **Each "restricted to N days/items" rule must have a boundary test**

### 4. Business Rule Validation Tests
- Each business rule gets at least one test that validates it works
- Each business rule gets at least one test that confirms it correctly blocks violations
- **Default value rules (e.g., "defaults to ALL when blank") must have an explicit test**

### 5. UI / Display Validation Tests
- Correct labels, error messages, and prompts displayed
- Loading states and confirmation dialogs
- Navigation and back-button behavior
- **Each UI control behavior (radio button parent/child logic, auto-populate) must be tested**

### 6. Integration / End-to-End Tests
- Full flow from start to finish
- Behavior when external system is unavailable
- Correct data passed between systems

---

## Step 4: Coverage Verification (MANDATORY)

After generating all test cases, you MUST perform a coverage check before writing the output script.

### How to verify:
1. Go through every REQ-XXX in your checklist
2. For each REQ, confirm at least one test case addresses it
3. If any REQ has no test case, you MUST add one before proceeding
4. Document any REQs that cannot be tested (e.g., ambiguous, pending bank confirmation) in the gap section

### Coverage must-checks:
- [ ] Every status value listed in the SRS has its own test case
- [ ] Every transaction type listed has at least one test case
- [ ] Every mandatory field has a negative test for missing input
- [ ] Every default value rule has a test verifying the default
- [ ] Every error message has a test verifying it appears
- [ ] Every UI behavior (radio buttons, auto-populate, masking) has a test
- [ ] Every "shall" statement in the SRS has at least one corresponding test case

---

## Step 5: Excel Output Format

### Azure DevOps Import Format
The Excel file must follow this exact structure, matching the column layout used for Azure DevOps Test Case import:

| Column | Header | Description |
|--------|--------|-------------|
| A | ID | Leave blank for new test cases (Azure DevOps assigns on import) |
| B | Work Item Type | Always `Test Case` for the parent row; leave blank for step rows |
| C | Title | Test case title for parent row; leave blank for step rows |
| D | Test Step | Step number (1, 2, 3...) for step rows; leave blank for parent row |
| E | Step Action | The action the tester performs; leave blank for parent row |
| F | Step Expected | The expected result of that step; leave blank for parent row |
| G | Area Path | Use the project area path from the SRS if available (e.g., `PHL-CTB-08-IB`) |
| H | State | Always `Ready` for new test cases |
| I | Complexity | Estimate: `1`=Simple, `3`=Medium, `5`=Complex |
| J | Assigned To | Leave blank unless specified |
| K | Status of automation | Always `Not yet automated` for newly generated test cases |

### Row Pattern
Each test case = 1 parent row + N step rows:

```
Row 1 (parent): ID=blank, WorkItemType=Test Case, Title=<test case name>, TestStep=blank, StepAction=blank, StepExpected=blank, AreaPath=<path>, State=Ready, Complexity=<1/3/5>, AssignedTo=blank, StatusOfAutomation=Not yet automated
Row 2 (step):   ID=blank, WorkItemType=blank, Title=blank, TestStep=1, StepAction=<action>, StepExpected=<expected result>, AreaPath=blank, State=blank, Complexity=blank, AssignedTo=blank, StatusOfAutomation=blank
Row 3 (step):   ID=blank, WorkItemType=blank, Title=blank, TestStep=2, StepAction=<action>, StepExpected=<expected result>, ...
...and so on
```

### Title Naming Convention
Use this pattern for test case titles:
`<Feature Name> [Sub-category if applicable] [Test Type if applicable] Verify <scenario description>`

**CRITICAL — the title prefix MUST be the actual functional requirement / feature name as stated in the SRS content, NOT the SRS document filename.**

When an SRS covers multiple functional requirements or features, each test case must be prefixed with the specific feature it belongs to. Do NOT use a single feature name or the SRS document name as a universal prefix for all test cases.

**How to determine the correct prefix:**
- Read the SRS section headings and functional requirement names
- Each distinct functional requirement / feature section gets its own prefix
- Use the feature name as it appears in the SRS (e.g., "Transaction History", "FO Reports")
- Add a sub-category in brackets if the feature has distinct sub-types (e.g., `[Piecemeal]`, `[Bulk]`)
- Add a test type tag if applicable (e.g., `[Negative]`, `[Boundary]`, `[UI]`)

**Multi-feature SRS example (4 functional requirements):**
- `Transaction History [Piecemeal] Verify Transaction History view displays Success status`
- `Transaction History [Piecemeal] [Negative] Verify user without function privilege cannot access Transaction History`
- `Bulk Fund Transfer Verify Bulk Fund Transfer view displays Success status`
- `Bulk Fund Transfer [Boundary] Verify bulk file with 1000 records downloads as 1 PDF with 1000 pages`
- `FO Reports [Piecemeal] Verify Channel filter is mandatory`
- `FO Reports [Bulk] [Negative] Verify error when Batch Reference ID is not provided`
- `Swift Charge Verify SWIFT Charge Option field is available when adding a Global Remittance counterparty`
- `Swift Charge [Negative] Verify system rejects record when charge option in template does not match counterparty record`

**Single-feature SRS example:**
- `P2M [Mobile: Android] Verify that a logged-in user can scan a valid BancNet partner merchant QRPH`
- `P2M [Mobile: Android] [Negative] Verify that the application displays an error prompt when a user scans an invalid QR code`

### Step Writing Guidelines

#### General Rules
- **Step Action**: Write in imperative form ("Enter", "Tap", "Navigate to", "Select", "Verify")
- **Step Expected**: Write from the user's perspective ("User sees", "System displays", "Transaction is", "Error message appears")
- Keep steps atomic — one action per step
- **Step 1 is ALWAYS the Prerequisite step** (see "Prerequisite / Test Data Step" section below). Step 2 is always the login step. Never combine login and prerequisites into one step.
- Include a verification/assertion step as the final step
- Steps must be detailed enough that a tester with **zero prior knowledge** of the feature can execute them without asking questions

#### Specificity Standard — NO VAGUE EXPECTED RESULTS (CRITICAL)
This is the most important quality rule. **Never write a vague expected result.** Every expected result must state *exactly* what the tester should see, read, or verify.

**❌ WRONG — too vague:**
> "System displays the transaction details correctly."
> "The Fund Transfer Advice shows the correct information."
> "User sees the transaction summary."

**✅ CORRECT — field-level specificity:**
> "System displays the Fund Transfer Advice page with the following details:
> - Reference Number: [the reference number of the transaction, e.g., 001242869]
> - UETR: [the UETR of the transaction, e.g., de2da6c9-18be-4848-b053-867ed90a316a]
> - Sender Name: [the sender name on the account, e.g., ABC Corporation]
> - Transaction Type: [as defined in the transaction, e.g., Local Remittance Fund Transfer]
> - Payment Channel: [e.g., PESONET]
> - Transaction Date: [the date the transaction was initiated, e.g., June 5, 2026]
> - Processing Date: [the date the bank processed the transaction, e.g., June 8, 2026]
> - Counterparty Name: [e.g., XYZ Corporation]
> - Counterparty Account Number: ********1378 (only the last 4 digits are visible; all preceding digits are masked with asterisks)
> - Bank Name: [e.g., BPI]
> - Transaction Amount: PHP12,345.99 (formatted with currency code and 2 decimal places)
> - Purpose of Transfer: [e.g., Payment to Supplier]
> - Payment Instruction: [e.g., Payment to Invoice 1234]
> - Status: Failed
> - Reason: RR-04-Rejected"

#### Rules for specific expected results:
1. **Display screens / detail pages**: Always enumerate every field label and its expected value or format. Do not say "all fields are correct."
2. **Masked data**: Explicitly describe the masking pattern (e.g., "only the last 4 digits are displayed, all preceding characters are replaced with asterisks `*`").
3. **Currency / numeric values**: State the exact format (e.g., "PHP12,345.99" — currency code prefix, comma thousands separator, 2 decimal places).
4. **Dates**: State the expected format (e.g., "June 5, 2026" — full month name, day, 4-digit year).
5. **Status values**: Spell out the exact status label as it appears in the UI (e.g., "Status: Failed", not just "transaction is failed").
6. **Error messages**: Quote the exact error message text as stated in the SRS. Do not paraphrase.
7. **Counts / limits**: State the exact number (e.g., "exactly 10 records are shown per page", not "records are paginated correctly").
8. **Buttons / links / controls**: Name the exact button label or control (e.g., "a 'Download PDF' button is visible and enabled", not "download option is available").
9. **Navigation**: State the exact page name or URL pattern the user lands on (e.g., "User is redirected to the Transaction History page", not "user is taken to the next page").
10. **Absence of elements**: When something should NOT appear, state it explicitly (e.g., "The 'Edit' button is not visible on this page.").

#### Laymanized but Complete
Write steps as if explaining to a smart colleague who has never used the system before. Avoid internal jargon unless it is a UI label:
- Say "Click on the 'Fund Transfer' menu item in the left navigation bar" — not "navigate to FT module"
- Say "Enter '12345.00' in the Amount field" — not "input a valid amount"
- Say "The page title reads 'Transaction History'" — not "the correct page is displayed"
- Use "you" or imperative form for actions, and "System" or "Page" for expected results

#### Prerequisite / Test Data Step (MANDATORY — ALWAYS Step 1)

**Every single test case MUST begin with a dedicated Step 1 that is explicitly labeled as the Prerequisite.**

This step is NEVER the login step. The Prerequisite step is ALWAYS Step 1. The login step is ALWAYS Step 2.

**Step 1 action format:**
> "Prerequisite: [describe what must exist or be deployed]. [List exact test data with specific values.]"

**Step 1 expected format:**
> "[One-line confirmation that the prerequisite is met, e.g., 'A SUCCESS piecemeal transaction is available.' or 'The SWIFT Charge Option feature is deployed.']"

**The Prerequisite step MUST describe:**
- **Feature deployment gate** — "The [feature name] feature must be deployed in the target environment." (required for every test case covering a new or enhanced feature)
- **The exact user role / account** needed (e.g., "A corporate user with Counterparty Maintenance function privilege (Maker role)")
- **Exact test data with realistic, specific values** — Reference Numbers (e.g., 001242869), Counterparty Names (e.g., 'ABC Global Corp'), Amounts (e.g., PHP12,345.99), Dates (e.g., June 5, 2026), UETRs (e.g., de2da6c9-18be-4848-8053-867ed90a316a), Account number endings (e.g., ending in 1378), Bank names (e.g., BPI)
- **The exact status or state** the transaction or record must be in (e.g., "A Piecemeal fund transfer transaction with 'Failed' status exists")
- **Record counts** for boundary tests (e.g., "A Bulk Fund Transfer batch containing exactly 50 records exists")

**Rules:**
- Do NOT fold the prerequisite into the login step or any other action step
- Do NOT write vague prerequisites like "Ensure conditions are met" or "Test data is available" — be specific about what those conditions are
- Do NOT skip the Prerequisite step even for simple tests
- The Prerequisite step action ALWAYS starts with the word **"Prerequisite:"**

**Example — correct:**
```
Step 1 Action:   Prerequisite: Ensure a Piecemeal fund transfer transaction with 'Success' status exists. Details: Ref No: 001242869, Sender: ABC Corporation, Counterparty: XYZ Corporation, Account ending 1378, Bank: BPI, Amount: PHP12,345.99, Channel: PESONET, Txn Date: June 5, 2026, Processing Date: June 8, 2026, UETR: de2da6c9-18be-4848-8053-867ed90a316a. The Fund Transfer Advice download feature must be deployed.
Step 1 Expected: The prerequisite 'Success' transaction exists and the feature is deployed.
Step 2 Action:   Log in to the CIB 2.0 portal using valid credentials of a corporate user with Transaction History function privilege.
Step 2 Expected: User is logged in and lands on the CIB 2.0 home dashboard.
```

**Example — wrong (do NOT do this):**
```
Step 1 Action:   Log in with valid credentials and ensure a transaction exists.   ← mixes login + prerequisite
Step 1 Expected: User is logged in.
```

---

## Step 6: Write and Run the Test Case Data Script

A reusable Excel generator already exists at `scripts/generate_testcases.py`.
**Do NOT recreate it.** It contains the `generate_test_cases_excel()` function with all formatting, headers, and Azure DevOps structure already handled.
A working example data script exists at `output/PHL-CTB-CIB-08-IB_SRS_v1.3_data.py` — use it as a reference for the expected pattern. This example demonstrates the correct prerequisite-first step structure, granular per-status tests, and all quality standards required.

Your only job is to create a small **data script** that imports and calls it.

### How to do it:

1. Create a new file named `output/<SRS_identifier>_data.py` (e.g., `output/PHL-CTB-CIB-08-IB_SRS_v1.3_data.py`)
2. Populate the `test_cases` list with the test cases you designed from the SRS analysis
3. Set `AREA_PATH` from the SRS document header/ID
4. Set `OUTPUT_PATH` to `output/<SRS_identifier>_TestCases.xlsx` (e.g., `output/PHL-CTB-CIB-08-IB_SRS_v1.3_TestCases.xlsx`)

**How to determine `<SRS_identifier>`:**
- Derive the identifier from the SRS PDF filename or document code — NOT from a single feature name
- If the SRS covers multiple features, use the SRS document's project code or full document name
- This ensures the file name represents the entire SRS, not just one feature within it
- Example: For `PHL-CTB-CIB-08-IB-Swift Charge_SRS_v1.3.pdf`, use `PHL-CTB-CIB-08-IB_SRS_v1.3` as the identifier
5. Run the script

### Data script template:

```python
import sys
import os
sys.dont_write_bytecode = True   # Prevent __pycache__ in scripts/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from generate_testcases import generate_test_cases_excel

AREA_PATH = ""        # Set from SRS, e.g., "PHL-CTB-CIB-08-IB"
OUTPUT_PATH = "output/<SRS_identifier>_TestCases.xlsx"  # Use SRS document code, not a single feature name

test_cases = [
    {
        "title": "Feature Verify happy path scenario",
        "complexity": "3",
        "steps": [
            {"action": "Login with valid credentials.", "expected": "User is logged in and lands on the home dashboard."},
            {"action": "Navigate to the target feature.", "expected": "Feature page is displayed correctly."},
            {"action": "Perform the main action with valid data.", "expected": "Action completes successfully and confirmation is shown."},
        ]
    },
    # ... add all generated test cases here
]

generate_test_cases_excel(test_cases, OUTPUT_PATH, AREA_PATH)
```

Then run it:
```
python output/<SRS_identifier>_data.py
```

---

## Step 7: Chat Summary

After generating the Excel file, provide a plain-language summary in this format:

---

### ✅ Test Cases Generated — Summary

**Feature covered:** [Feature name from SRS]
**Total test cases:** [number]
**Output file:** `output/<filename>.xlsx`

#### Requirements Checklist Coverage:
State the total number of REQ items extracted and how many are covered (e.g., "47/47 requirements covered").

#### What's covered:

**Happy Path ([n] test cases)**
Plain English list of what normal/successful flows were tested.

**Negative / Error Scenarios ([n] test cases)**
Plain English list of what failure scenarios were tested.

**Boundary / Edge Cases ([n] test cases)**
Plain English list of what boundary conditions were tested.

**Business Rules ([n] test cases)**
Plain English list of which business rules were validated.

**Integration / End-to-End ([n] test cases)**
Plain English list of full-flow tests included.

#### What's NOT covered (known gaps):
List anything from the SRS that could not be tested due to ambiguity, missing information, or out-of-scope items. Reference the REQ-XXX number for each gap.

---

## Important Rules

- Always extract the **Area Path** from the SRS document header or metadata if present (e.g., `PHL-CTB-08-IB`)
- Never fabricate requirements — only generate test cases for what is explicitly stated or clearly implied in the SRS
- When a requirement is ambiguous, generate the most reasonable interpretation AND add a comment/note in the gap section
- **Every distinct status value listed in the SRS must have its own dedicated test case** — never combine multiple statuses into one test
- **Every distinct transaction type listed in the SRS must have at least one test case** — if a type also has currency variants (PHP vs USD), each currency gets its own test case
- **Download / action button availability must be tested per each distinct status** — if a button should be accessible regardless of status, write one test per status to confirm
- **iCare / Service Request manual update scenarios that affect both batch and record level must be split into two separate test cases** — one for batch level, one for record level
- **Backward compatibility scenarios (e.g., existing records getting a new default value after an enhancement) must have dedicated test cases** — both for the default value itself and for confirming the record can still be used in downstream flows
- **Each selectable option in a multi-option field (e.g., OUR / BEN / SHA) must have its own test case for individual selection**
- **Negative privilege tests must be written for every module** — one test per module for a user without the required function privilege
- Aim for **thorough coverage** — a complete SRS should produce at minimum 30–80 test cases depending on complexity; do not stop early
- Steps should be detailed enough for a manual tester with **zero prior context** to execute them
- The output Excel file must be importable into Azure DevOps without modification
- **Do not consider the task complete until the Coverage Verification checklist in Step 4 is fully satisfied**

### Specificity Non-Negotiables (Senior QA Standard)
These rules are absolute. Violating any of them means the test case is not production-ready:

1. **No vague expected results.** "System displays the details correctly" is never acceptable. Every display validation must enumerate the fields and their expected values or formats.
2. **Field-level validation on detail/summary screens.** When a test case verifies a summary, advice, or detail page, the expected result must list every field shown on that screen with its label, expected value (or format if value is dynamic), and any display rules (e.g., masking, currency prefix, date format).
3. **Masked fields must describe the masking pattern explicitly.** State how many characters are masked, which characters are visible, and what the mask character is (e.g., "Counterparty Account Number displays as `********1378` — only the last 4 digits are visible; all preceding digits are replaced with `*`").
4. **Error messages must be quoted verbatim** from the SRS. Never paraphrase error text.
5. **Exact button/link labels must be named.** "A button is available" is not acceptable. Name the exact label: "A 'Submit' button is visible and enabled."
6. **Exact page/screen names must be stated.** "User is taken to the next screen" is not acceptable. Name the screen: "User is navigated to the 'Fund Transfer Advice' page."
7. **Test data must be realistic and representative.** Use plausible sample values in prerequisites and steps (e.g., specific reference numbers, realistic amounts, real bank names) so the tester understands the shape of the data they are working with.
8. **Every test case must stand alone.** A tester picking up any single test case should be able to execute it without reading other test cases — all setup, navigation, and data requirements must be self-contained in that test case's steps.
