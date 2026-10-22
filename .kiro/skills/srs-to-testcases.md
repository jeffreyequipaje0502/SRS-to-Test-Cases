---
inclusion: auto
name: srs-to-testcases
description: Activated when the user asks to generate test cases, create test scenarios, or analyze an SRS or requirements document. Provides the full workflow for producing an Azure DevOps-importable .xlsx file from a PDF SRS.
---

# Skill: SRS to Test Cases Generator

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
- **Each distinct transaction type must have at least one test case**

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
`[Feature] [Platform if applicable] <Scenario description>`

Examples:
- `Swift Charge Verify that a logged-in user can initiate a charge request with valid amount`
- `Swift Charge [Negative] Verify that system displays error when amount exceeds daily limit`
- `Swift Charge [Boundary] Verify minimum transaction amount is accepted`

### Step Writing Guidelines
- **Step Action**: Write in imperative form ("Enter", "Tap", "Navigate to", "Select", "Verify")
- **Step Expected**: Write from the user's perspective ("User sees", "System displays", "Transaction is", "Error message appears")
- Keep steps atomic — one action per step
- Include a prerequisite/setup step (Step 1) when needed (e.g., "Login with valid credentials")
- Include a verification/assertion step as the final step

---

## Step 6: Write and Run the Test Case Data Script

A reusable Excel generator already exists at `scripts/generate_testcases.py`.
**Do NOT recreate it.** It contains the `generate_test_cases_excel()` function with all formatting, headers, and Azure DevOps structure already handled.
A working example data script exists at `output/SwiftCharge_example_data.py` — use it as a reference for the expected pattern.

Your only job is to create a small **data script** that imports and calls it.

### How to do it:

1. Create a new file named `output/<SRS_name>_data.py` (e.g., `output/SwiftCharge_data.py`)
2. Populate the `test_cases` list with the test cases you designed from the SRS analysis
3. Set `AREA_PATH` from the SRS document header/ID
4. Set `OUTPUT_PATH` to `output/<SRS_name>_TestCases.xlsx`
5. Run the script

### Data script template:

```python
import sys
import os
sys.dont_write_bytecode = True   # Prevent __pycache__ in scripts/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from generate_testcases import generate_test_cases_excel

AREA_PATH = ""        # Set from SRS, e.g., "PHL-CTB-CIB-08-IB"
OUTPUT_PATH = "output/SRS_TestCases.xlsx"  # Update with actual SRS name

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
python output/<SRS_name>_data.py
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
- **Every distinct transaction type listed in the SRS must have at least one test case**
- Aim for **thorough coverage** — a complete SRS should produce at minimum 30–80 test cases depending on complexity; do not stop early
- Steps should be detailed enough for a manual tester with no context to execute them
- The output Excel file must be importable into Azure DevOps without modification
- **Do not consider the task complete until the Coverage Verification checklist in Step 4 is fully satisfied**
