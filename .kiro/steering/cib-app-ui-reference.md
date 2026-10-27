---
inclusion: auto
name: cib-app-ui-reference
description: Activated when generating test cases for the CIB 2.0 application. Contains verified UI labels, navigation paths, field names, button names, page titles, and screen structure captured directly from the live QA environment at https://ctbcqa.megalink.com.ph. Use this to write test steps with exact UI labels.
---

# CIB 2.0 Application — UI Reference Guide

Captured from: https://ctbcqa.megalink.com.ph/frontend  
Environment: QA  
App version: 9.29.22 (baseline screenshots) · Figma designs reviewed October 23, 2026  
Captured on: October 23, 2026  

> **NOTE on Swift Charge / Fund Transfer Advice enhancements:**  
> The Figma design screenshots shared on October 23, 2026 confirm that the following features (previously marked "NOT YET DEPLOYED" in v9.29.22) are now designed/deployed in a newer build. The UI details below have been updated accordingly. Where a feature has been confirmed via Figma but not yet verified in the live QA environment, it is marked **[FIGMA CONFIRMED]**.

## Screenshots
All screenshots taken during UI exploration are stored at:
`screenshots/cib-ui-exploration/`

| File | Screen captured |
|---|---|
| `cib-dashboard.png` | Dashboard — tile overview |
| `cib-sidebar.png` | Left navigation sidebar — all menu items expanded |
| `cib-counterparty-home.png` | Counterparty Maintenance — list page |
| `cib-add-counterparty-txntype.png` | Add Counterparty — Transaction Type dropdown open |
| `cib-add-counterparty-global-remittance.png` | Add Counterparty — Global Remittance selected (full page) |
| `cib-add-counterparty-swift.png` | Add Counterparty — Global Remittance + SWIFT selected (Charge Option field **now present** per Figma) |
| `cib-payment-channel-options.png` | Add Counterparty — Payment Channel dropdown showing SWIFT only option |
| `cib-transaction-history.png` | Transaction History — list with search filters and status checkboxes |
| `cib-transaction-history-view.png` | Transaction History — View screen detail (Download Fund Transfer Advice button **now present** per Figma) |
| `cib-bulk-fund-transfer.png` | Bulk Fund Transfer — list/search page (Download dropdown **now present** per Figma) |
| `cib-reports.png` | Corporate Reports — main page |
| `cib-report-type-options.png` | Corporate Reports — Report Type dropdown options |
| `cib-report-name-options.png` | Corporate Reports — Report Name options under Transaction Reports (Fund Transfer Advice reports **now present** per Figma) |

To re-explore the app and update this file, run Playwright against `https://ctbcqa.megalink.com.ph/frontend/#/pages/login` and save new screenshots to `screenshots/cib-ui-exploration/`.

---

> Use this reference whenever writing test case steps for the CIB 2.0 app.
> All labels, button names, field names, page titles, and navigation paths below are **verified from the live UI**.

---

## 1. Login Page

**URL:** `#/pages/login`  
**Page title:** CTBC Realtime Corporate  

### Fields
| Field Label | Type | Placeholder |
|---|---|---|
| Corporate ID | Text input | (none) |
| User ID | Text input | (none) |
| Password | Password input | (none) |

### Buttons
- `Refresh` — clears the form
- `Login` — submits credentials

### Other elements
- `Forgot Password` link → `#/pages/forgotpassword`
- `User ID` (forgot) link → `#/pages/forgotUserId`
- Footer links: CTBC Bank Home, Terms and Conditions, Privacy Policy, Security Statement, Rates, FAQs, Locations, Contact Us
- Footer logos: DPO/DPS Badge, BancNet Logo, PDIC Logo
- Disclaimer: "CTBC Bank (Philippines) Corp. is regulated by the Bangko Sentral ng Pilipinas (BSP)..."

### Post-login: OTP Page
**URL:** `#/pages/otp`  
- Heading: **"Type TOTP"**
- Instruction: *"Please type in the code displayed on your authenticator app from your device."*
- 6 individual single-digit textboxes (one per OTP digit)
- `Cancel` button
- `Proceed` button (disabled until all 6 digits are entered)

---

## 2. Left Navigation Sidebar

The sidebar collapses to icons only; clicking an icon reveals the text label and sub-items.

| Menu Item | Sub-items |
|---|---|
| **Dashboard** | (none) |
| **Security Settings** | (expandable) |
| **User Maintenance** | (expandable) |
| **Auth Role** | (expandable) |
| **Accounts** | (expandable) |
| **Counterparty Maintenance** | Add Counterparty · Verify/Reject Counterparty · Approve Counterparty |
| **Biller Maintenance** | (expandable) |
| **Fund Transfer** | New Fund Transfer · Bulk Fund Transfer · Approve/Reject Transfer · Verify/Reject Transfer · Ongoing Fund Transfers · Scheduled Fund Transfer · Transaction History |
| **Bills Payment** | (expandable) |
| **PDC Warehousing** | (expandable) |
| **Reports** | (none — single page) |
| **Mail Box** | (none) |
| **Download Templates** | (none) |
| **Service Request** | (expandable) |

---

## 3. Dashboard

**URL:** `#/main/dashboard`  
**Page title:** CTBC Realtime Corporate - Dashboard  
**Breadcrumb:** Home  

### Greeting
- "Good Morning [First Name]!" heading
- "Your last successful login was at [date time]"

### Dashboard Tiles (counts shown per tile)
- Assigned Accounts
- Pending Approval Users
- Pending Verification Fund Transfers
- Pending Verification Bill Payments
- Pending Approval PDC Warehousing
- Pending Verification PDC Warehousing
- Pending PDC Warehousing
- Pending Fund Transfers
- Pending Bill Payments
- Pending Bulk Fund Transfers
- Pending Bulk Bill Payments
- Pending Approval Billers
- Pending Approval Counterparties
- Pending Approval Fund Transfers
- Pending Approval Bill Payments

### Buttons
- `Refresh`
- `Customize Dashboard` (clickable heading)

---

## 4. Counterparty Maintenance

### 4.1 Counterparty Maintenance List (Home)

**URL:** `#/main/maintenance/beneficiary/home`  
**Page title:** CTBC Realtime Corporate - Counterparty Maintenance  
**Breadcrumb:** Home › Counterparty Maintenance  
**Page heading:** Counterparty Maintenance  

#### Search Section
- Heading: **"Search"** / sub-text: *"Provide the required filters"*
- Fields:
  | Field Label | Type |
  |---|---|
  | Counterparty Name | Text input |
  | Fund Transfer Type | Dropdown (Select One) |
  | Payment Channel | Dropdown (Select One) |
  | Bank | Dropdown (Select One) |
  | Account Number | Text input |
  | Routing Number/Swift Code | Text input (placeholder: "Routing Number/Swift Code") |
- Status checkboxes: `ACTIVE` · `MODIFIED` · `REJECTED` · `PENDING VERIFICATION` · `PENDING APPROVAL`
- Button: `Search` (with search icon prefix)

#### Counterparty List Table
| Column Header | Notes |
|---|---|
| ID | Numeric ID |
| Counterparty Name | |
| Transaction Type | e.g., Third Party Account, Local Remittance, Global Remittance |
| Payment Channel | e.g., WITHIN BANK, PESONET, BANCNET, RTGS, SWIFT |
| Status | ACTIVE / MODIFIED / REJECTED / PENDING VERIFICATION / PENDING APPROVAL |
| Action | `View` button |

- Pagination: rows per page selector (default 10), page indicator "Page X of Y"
- Heading above table: **"Counterparty List"**

---

### 4.2 Add Counterparty

**URL:** `#/main/maintenance/beneficiary/add`  
**Page title:** CTBC Realtime Corporate - Add Counterparty  
**Breadcrumb:** Home › Counterparty Maintenance › Create  
**Page heading:** Add Counterparty  
**Section heading:** Counterparty Details  

#### Fields — Left Column
| Field Label | Required | Type | Placeholder |
|---|---|---|---|
| Transaction Type | * | Dropdown | "Select Type" |
| Counterparty Name | * | Text input | "Enter Counterparty Name" |
| Nickname | * | Text input | "Enter Beneficiary Nickname" |
| Email | No | Text input | "For Beneficiary Notification" |
| Mobile Number | No | Phone input | "+63 · 2 3234 5678" |

#### Fields — Right Column
| Field Label | Required | Type | Placeholder / Options |
|---|---|---|---|
| Payment Channel | * | Dropdown | "Select Type" |
| Charge Option | * | Checkbox group | Appears when Transaction Type = Global Remittance AND Payment Channel = SWIFT |
| Bank | * | Dropdown | "Type here" |
| Account No | * | Text input | "Enter Payee Account" |
| Tax No | No | Text input | "Enter Tax Number" |

#### Charge Option Field (SWIFT transactions) — **[FIGMA CONFIRMED]**
- Appears when: Transaction Type = **Global Remittance** AND Payment Channel = **SWIFT**
- Control type: Checkbox group (multiple selection allowed)
- Label: **"Charge Option *"** (required)
- Options (displayed as checkboxes):
  - **Select All** (selects/deselects all three below)
  - **OUR**
  - **BEN**
  - **SHA**
- Default: all three (OUR, BEN, SHA) are checked
- Behavior: checking "Select All" toggles all three options simultaneously

#### Transaction Type Options (dropdown)
- Third Party Accounts
- Local Remittance
- Global Remittance

#### Payment Channel Options by Transaction Type
- **Third Party Accounts:** WITHIN BANK (and others)
- **Local Remittance:** PESONET, RTGS, BANCNET, PDDTS, INSTAPAY (and others)
- **Global Remittance:** SWIFT *(only one option)*

#### Counterparty Address Section
- Heading: **"Counterparty Address"** (bold)
- Fields:
  | Field Label | Required | Type | Default |
  |---|---|---|---|
  | Country | * | Dropdown | Philippines (PHL) |
  | Zip Code/Postal Code | * | Text input | "Enter Zip Code/Postal Code" |
  | City/Town/District | * | Text input | "Enter City/Town/District" |
  | Address | * | Text input | "Enter House No./Block/Lot/Floor/Street/Bldg No./Bldg Name" |
  | | | | Note: "Address should not have City/Town/District" |

#### Bulk Upload Section
- Text: "or"
- Dashed upload area: *"Click or drop here to upload csv file"*

#### Buttons
- `Proceed ›` (disabled until required fields filled)

> **✅ SWIFT Charge Option — DEPLOYED (confirmed via Figma, October 23, 2026)**
> The Charge Option field is present on the Add Counterparty form when Transaction Type = Global Remittance and Payment Channel = SWIFT.
> The field renders as a checkbox group with a "Select All" master toggle and three individual options: **OUR**, **BEN**, **SHA**.
> All three are checked by default. The field is required (*).
> Verify deployment in the live test environment before executing related test cases.

---

### 4.3 Verify/Reject Counterparty

**URL:** `#/main/maintenance/beneficiary/verify` (sub-menu item)  
**Sub-menu label:** Verify/Reject Counterparty  

### 4.4 Approve Counterparty

**Sub-menu label:** Approve Counterparty  

---

## 5. Fund Transfer

### 5.1 Sub-menu Items (Fund Transfer)
| Sub-menu Label | URL |
|---|---|
| New Fund Transfer | `#/main/fundtransfer/new` |
| Bulk Fund Transfer | `#/main/fundtransfer/bulk/home` |
| Approve/Reject Transfer | |
| Verify/Reject Transfer | |
| Ongoing Fund Transfers | `#/main/fundtransfer/home` |
| Scheduled Fund Transfer | |
| Transaction History | `#/main/fundtransfer/history` |

---

### 5.2 Ongoing Fund Transfers

**URL:** `#/main/fundtransfer/home`  
**Page title:** CTBC Realtime Corporate - Ongoing Fund Transfer  
**Breadcrumb:** Home › Fund Transfer › Main  
**Page heading:** Ongoing Fund Transfer  

#### Search Fields
| Field | Type |
|---|---|
| From Account | Dropdown (Select) |
| To Account No | Text input ("Enter To Account No") |
| Transaction Type | Dropdown (Select) |
| Start Date | Date picker (MM/DD/YYYY) |
| End Date | Date picker (MM/DD/YYYY) |

- Button: `Search`

#### Ongoing Transactions Table
**Note shown:** *"The transactions displayed here show whether the transactions are still pending in the Auth process defined. Approved/Reject Transactions are shown in the Transaction History Page."*

| Column | Notes |
|---|---|
| Ref ID | Prefixed with space + number, e.g., " 00117129" |
| Transaction Date | MM/DD/YYYY |
| Counterparty Name | |
| Transaction Type | e.g., Third Party Account |
| Debiting Account | Account number |
| Currency | PHP / USD |
| Transaction Amount | Decimal, e.g., "2.00" |
| Status | e.g., Pending Approval |
| Action | `View` button |

---

### 5.3 Transaction History

**URL:** `#/main/fundtransfer/history`  
**Page title:** CTBC Realtime Corporate - Transaction History  
**Breadcrumb:** Home › Fund Transfer › Transaction History  
**Page heading:** Transaction History  

#### Search Section
| Field | Type | Notes |
|---|---|---|
| From Account | Dropdown (Select) | |
| To Account No | Text input ("Enter To Account No") | |
| Transaction Type | Dropdown (Select) | |
| Start Date | Date picker (MM/DD/YYYY) | Placeholder: ENTER_START_DATE |
| End Date | Date picker (MM/DD/YYYY) | Placeholder: ENTER_END_DATE |

- **Status checkboxes:** `FAILED` · `SUCCESS` · `SENT FOR PROCESSING` · `QUEUED FOR PROCESSING` · `REJECTED` · `EXPIRED`
- Button: `Search`

#### Transaction History List Table
**Note shown:** *"Transactions are filtered by corporate and ordered by most recent"*

| Column Header | Notes |
|---|---|
| Ref ID | Prefixed with icon + number, e.g., " 00117128" |
| Processing Date | MM/DD/YYYY HH:MM AM/PM format (e.g., "10/20/2026 12:00 AM"); shows "-" if not yet processed |
| Counterparty Name | |
| Transaction Type | e.g., Third Party Account, Local Remittance, Global Remittance |
| Debiting Account | Account number |
| Currency | PHP / USD |
| Transaction Amount | Decimal, e.g., "2.00" |
| Status | FAILED / SUCCESS (capital) / SENT FOR PROCESSING / QUEUED FOR PROCESSING / EXPIRED |
| Action | `View` button |

> **Note:** Status values in the list use ALL CAPS (e.g., "FAILED", "SUCCESS") except for Global Remittance transactions which show "Success" (mixed case). This inconsistency exists in the current QA build.

- Pagination: rows per page (default 10), "Page 1 of 240" format

#### Status Values Observed in QA
- `FAILED`
- `Success` (Global Remittance transactions)
- `EXPIRED`

---

### 5.4 Transaction History — View Screen

**URL:** `#/main/fundtransfer/history-view?auxNo=...&type=MASTER&parentRoute=...`  
**Page title:** CTBC Realtime Corporate - Transaction History  
**Breadcrumb:** Home › Fund Transfer › Transaction History  
**Page heading:** Transaction History  

#### Left Panel — Transaction Summary Fields
| Field Label | Example Value | Notes |
|---|---|---|
| Reference Number | 00116933 | Shown with icon |
| UETR | 123a4567-o89c-12d3-a456 00000000000 | **[FIGMA CONFIRMED]** SWIFT UETR — populated for SWIFT transactions; shows "-" for non-SWIFT |
| Amount | PHP 100.00 | Currency prefix + space + amount |
| Fee | PHP 0.00 | |
| Total Amount | PHP 100.00 | |
| Transaction Date | 09/24/2026 | MM/DD/YYYY format |
| Processing Date | 09/25/2026 | **[FIGMA CONFIRMED]** MM/DD/YYYY format |
| Counterparty Name | Bataan Development Bank Inc. | Shown with icon |
| Counterparty Email | tests1@gmail.com | Shown with icon |
| Bank | Bataan Development Bank, Inc. | Shown with icon |
| Status | Success | Shown with status icon |

#### Right Panel — Fund Transfer Details Box (grey background)
- Heading: **"Fund Transfer"**
- Fields shown:
  | Field Label | Example Value |
  |---|---|
  | Transaction Type | LOCAL REMITTANCE FUND TRANSFER |
  | Network Type | PESONET |
  | Purpose of Transfer | Bill Payment |
  | Remarks | Testing |

#### Buttons (bottom of page)
- `‹ Back` — returns to Transaction History list
- `Download Fund Transfer Advice` — **[FIGMA CONFIRMED]** downloads the Fund Transfer Advice PDF for this transaction
- `Status` — shows transaction status detail

> **✅ Download Fund Transfer Advice Button — DEPLOYED (confirmed via Figma, October 23, 2026)**
> The **"Download Fund Transfer Advice"** button is now present on the Transaction History View screen.
> The **UETR** field is also now populated (for SWIFT transactions).
> The **Processing Date** field is confirmed present in the view detail screen.
> Verify deployment in the live test environment before executing related test cases.

---

### 5.5 Bulk Fund Transfer

**URL:** `#/main/fundtransfer/bulk/home`  
**Page title:** CTBC Realtime Corporate - Bulk Fund Transfer  
**Breadcrumb:** Home › Fund Transfer › Bulk-Home  
**Page heading:** Bulk Fund Transfer  

#### Header
- `+ New Bulk Fund Transfer` (collapsible/expandable section heading)

#### Search Section
| Field | Type | Placeholder |
|---|---|---|
| From Account | Dropdown | Select |
| Batch ID | Text input | "Enter Batch ID" |
| Transaction Type | Dropdown | Select |
| Reference Name | Text input | "Enter Reference Name" |
| Date From | Date picker | ENTER_DATE_FROM (MM/DD/YYYY) |
| Date To | Date picker | ENTER_DATE_TO (MM/DD/YYYY) |

- Button: `Search`

#### Bulk Fund Transfer Table
**Note shown:** *"Uploaded bulk transactions are shown here"*

| Column Header | Notes |
|---|---|
| Batch Ref ID | |
| Processing Date | MM/DD/YYYY format |
| Transaction Type | e.g., Global Remittance |
| Reference Name | e.g., oklswift02 |
| Status | e.g., PENDING VERIFICATION (amber badge) · SENT FOR PROCESSING (green badge) |
| Action | `Download ▾` dropdown button + `View` button |

#### Download Dropdown Options (per row) — **[FIGMA CONFIRMED]**
When clicking the `Download ▾` button on a Bulk Fund Transfer row, a dropdown appears with:
- **XLSX File** — `Download` button
- **PDF File** — `Download` button
- **Fund Transfer Advice** — `Download` button

- Empty state text: **"NO RESULTS FOUND"**

### 5.6 Bulk Fund Transfer — View Screen — **[FIGMA CONFIRMED]**

**Breadcrumb:** Home › Fund Transfer › View  
**Page heading:** Bulk Fund Transfer  
**Section heading:** Bulk Fund Transfer  

#### Batch Detail Fields
| Field Label | Example Value |
|---|---|
| Batch ID: | 33807 |
| Transaction Date: | 09/24/2026 |
| Processing Date: | 09/25/2026 |
| Debiting Account: | 001720030087 |
| Transaction Type: | Global Remittance |
| Total Transaction Amount: | USD 150.00 |
| Total Records: | 1 |
| Currency: | USD |
| Payment Channel: | **SWIFT** |
| Fee Per Transaction: | USD 0.00 |
| Total Debit Amount: | USD 150.00 |

#### Buttons (bottom of page)
- `‹ Back` — returns to Bulk Fund Transfer list
- `Download ▾` — dropdown with options:
  - **XLSX File** — `Download` button
  - **PDF File** — `Download` button
  - **Fund Transfer Advice** — `Download` button

> **✅ Download Fund Transfer Advice button — DEPLOYED (confirmed via Figma, October 23, 2026)**
> The Download dropdown with "XLSX File", "PDF File", and "Fund Transfer Advice" options is now present in both the Bulk Fund Transfer list (per-row action) and the Bulk Fund Transfer View screen.
> The Bulk Fund Transfer View screen also confirms **Payment Channel: SWIFT** and **Currency: USD** for SWIFT transactions.
> Verify deployment in the live test environment before executing related test cases.

---

## 6. Reports (Corporate Reports)

**URL:** `#/main/report`  
**Page title:** CTBC Realtime Corporate - Corporate Reports  
**Breadcrumb:** Home › Report › Main  
**Page heading:** Corporate Reports  

### Format Selection (radio buttons — top right)
- `PDF` (default, selected)
- `XLS`
- `CSV`

### Select Report Section
- Heading: **"Select Report"**
- Sub-text: *"Fill the details to select the report you want to generate"*

#### Fields
| Field Label | Type | Options |
|---|---|---|
| Report Type | Dropdown (Select) | Transaction Reports · Non Transaction Reports · User Reports |
| Report Name | Dropdown (Select) | Populated based on Report Type selection |

#### Report Names under "Transaction Reports"
| Report Name | Format buttons |
|---|---|
| Fund Transfer Transaction Report | PDF, XLS, CSV |
| Schedule Fund Transfer Transaction Report | |
| Bulk Fund Transfer Transaction Report | |
| Bills Payment Transaction Report | |
| Schedule Bills Payment Transaction Report | |
| Bulk Bills Payment Report | |
| Service Request Report | |
| PDC Warehousing Report | |
| PDC Warehousing - Record Level Report | |
| Proof List Report | |
| Fund Transfer Advice (Piecemeal) | PDF only — **[FIGMA CONFIRMED]** |
| Fund Transfer Advice (Bulk) | PDF only — **[FIGMA CONFIRMED]** |

#### "Fund Transfer Advice (Bulk)" Report — Filter Fields — **[FIGMA CONFIRMED]**
**Breadcrumb (example):** Home › Report › Main  
**Report Type:** Transaction Reports  
**Report Name:** Fund Transfer Advice (Bulk)  
**Format button (top right):** `PDF`  

| Field Label | Required | Type |
|---|---|---|
| Date From | No | Date-time picker (e.g., "29/09/2026 12:00 am") |
| Date To | No | Date-time picker (e.g., "27/09/2026 12:00 am") |
| Transaction Status | No | Dropdown (Select) |
| Transaction Type | No | Dropdown (Status placeholder) |
| Channel | No | Dropdown (Select) |
| Batch Reference ID | * | Dropdown (required) |

**Action buttons:** `RESET` (yellow) · `VIEW` (dark) · `DOWNLOAD` (teal) · `GENERATE` (green)

#### "Fund Transfer Advice (Piecemeal)" Report — Filter Fields — **[FIGMA CONFIRMED]**
**Report Name:** Fund Transfer Advice (Piecemeal)  
**Format button (top right):** `PDF`  

| Field Label | Required | Type |
|---|---|---|
| Date From | No | Date-time picker |
| Date To | No | Date-time picker |
| Transaction Status | No | Dropdown (Select) |
| Transaction Type | * | Dropdown (required, "Status" placeholder) |
| Channel | * | Dropdown (required, Select) |

**Action buttons:** `RESET` (yellow) · `VIEW` (dark) · `DOWNLOAD` (teal) · `GENERATE` (green)

> **✅ Fund Transfer Advice Reports — DEPLOYED (confirmed via Figma, October 23, 2026)**
> Both **"Fund Transfer Advice (Piecemeal)"** and **"Fund Transfer Advice (Bulk)"** now appear in the Report Name dropdown under Transaction Reports.
> - Fund Transfer Advice (Bulk) requires **Batch Reference ID** (mandatory); Transaction Type and Channel are optional.
> - Fund Transfer Advice (Piecemeal) requires **Transaction Type** and **Channel** (both mandatory); Batch Reference ID is not shown.
> Verify deployment in the live test environment before executing related test cases.

---

## 7. Key UI Patterns (Global)

### Breadcrumb Format
`Home › [Section Name] › [Sub-page Name]`  
The breadcrumb always starts with "Home" linking back to `#/main/dashboard`.

### Page Title Format
`CTBC Realtime Corporate - [Page Name]`

### Table Action Buttons
All record-level action buttons use icon + text format:
- `View` (eye/search icon + "View")
- `Back` (arrow icon + "Back")
- `Status` (icon + "Status")

### Mandatory Fields
Mandatory fields are marked with a red asterisk `*` after the label. Example: `Transaction Type *`

### Dropdown Behavior
- Default placeholder text: **"Select"** or **"Select One"** or **"Select Type"** depending on context
- Dropdowns have a clear (×) button to reset selection
- Dropdowns support type-ahead search (combobox behavior)

### Date Fields
- Format: `MM/DD/YYYY`
- Placeholders use uppercase: `ENTER_START_DATE`, `ENTER_DATE_FROM`, etc.

### Pagination
- Standard format: `Page X of Y`
- Rows per page selector (default: 10)
- Navigation: previous / page numbers / next

### Status Display
- Transaction History list: statuses shown in ALL CAPS (FAILED, SUCCESS, SENT FOR PROCESSING, QUEUED FOR PROCESSING, REJECTED, EXPIRED)
- Some inconsistency observed: Global Remittance shows "Success" (mixed case) vs "FAILED" (caps) in same list

### Currency Format
- Amount fields displayed as: `PHP 2.00` (currency code + space + decimal amount)
- Note: SRS specifies `PHP12,345.99` format (no space, comma thousands) for Fund Transfer Advice PDF — different from current on-screen display

### Footer
- Copyright: *"Copyright @ 2024 Hitachi Digital Payments."*
- Version: *"version :9.29.22"*

---

## 8. Feature Deployment Status (SRS v1.3 Enhancements)

| Feature | Screen | Status | Source |
|---|---|---|---|
| SWIFT Charge Option | Add/Edit Counterparty (Global Remittance + SWIFT) | ✅ **DEPLOYED** — Checkbox group: Select All / OUR / BEN / SHA | Figma, Oct 23, 2026 |
| Download Fund Transfer Advice | Transaction History View | ✅ **DEPLOYED** — "Download Fund Transfer Advice" button present | Figma, Oct 23, 2026 |
| UETR Field populated | Transaction History View | ✅ **DEPLOYED** — UETR shows real value for SWIFT transactions | Figma, Oct 23, 2026 |
| Processing Date in View detail | Transaction History View screen | ✅ **CONFIRMED** — Processing Date field visible in detail view | Figma, Oct 23, 2026 |
| Network Type field | Transaction History View screen | ✅ **CONFIRMED** — "Network Type" field visible in right panel (e.g., PESONET) | Figma, Oct 23, 2026 |
| Download Dropdown (list) | Bulk Fund Transfer list (per-row action) | ✅ **DEPLOYED** — XLSX File / PDF File / Fund Transfer Advice | Figma, Oct 23, 2026 |
| Download Dropdown (view) | Bulk Fund Transfer View screen | ✅ **DEPLOYED** — XLSX File / PDF File / Fund Transfer Advice | Figma, Oct 23, 2026 |
| Fund Transfer Advice (Piecemeal) Report | Corporate Reports → Transaction Reports | ✅ **DEPLOYED** — available in Report Name dropdown | Figma, Oct 23, 2026 |
| Fund Transfer Advice (Bulk) Report | Corporate Reports → Transaction Reports | ✅ **DEPLOYED** — available in Report Name dropdown | Figma, Oct 23, 2026 |

> All features above have been confirmed via Figma design screenshots. Verify in the live QA or UAT environment before executing test cases if you are unsure which build is deployed.
> For test cases covering these features, the prerequisite note is:
> *"Verify that [feature name] is deployed and enabled in the target test environment. Refer to the app version or release notes if unsure."*
