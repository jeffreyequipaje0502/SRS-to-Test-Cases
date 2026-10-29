---
inclusion: auto
name: rib-app-ui-reference
description: Activated when generating test cases for the RIB (CTBC NetBanking / Retail Internet Banking) application. Contains verified UI labels, navigation, field names, button names, page titles/routes, and screen structure captured directly from the live QA environment at https://ctbcqa.megalink.com.ph/web/. Use this to write test steps with exact UI labels.
---

# RIB — CTBC NetBanking (Retail Internet Banking) — UI Reference Guide

Captured from: https://ctbcqa.megalink.com.ph/web/
Environment: QA
App version: 1.1.974066 (shown bottom-left banner on every screen and on My Profile)
Captured on: October 29, 2026
Logged-in test user: Raymund PEREZ

> **IMPORTANT — technology note:**
> The RIB NetBanking app is a **Flutter web app** (it renders to a drawing surface via `main.dart.js`, not an HTML DOM). It is fronted by a **Cloudflare Turnstile** challenge on login.
> Because of this:
> - There is **no HTML DOM** with conventional input/button elements. Labels below were verified from **live screenshots** plus Flutter's **accessibility semantics tree** (enabled on demand).
> - The `Page Title` values below double as the **in-app route** (the Flutter app writes the current route into `document.title`, e.g. `/dashboard/home/send-money`). These are verified and useful for automation, but they are internal Flutter routes, not navigable URLs — every screen lives under the single URL `https://ctbcqa.megalink.com.ph/web/`.
> - **Do NOT use browser Back/refresh** during a session: the app loads `back_button_logout.js` and will log the user out. Navigate only via in-app controls (sidebar, Quick Actions, in-screen back arrows).

## Screenshots
All screenshots taken during UI exploration are stored at:
`screenshots/rib-ui-exploration/`

| File | Screen captured |
|---|---|
| `rib-login.png` | Login page (NetBanking) with Cloudflare Turnstile |
| `rib-dashboard.png` | Dashboard — greeting, Quick Actions, Accounts, Recent Transactions, Promotions |
| `rib-my-accounts.png` | My Accounts — account list with Filter / View All |
| `rib-fund-transfer.png` | Fund Transfer landing — Direct Transfer / Own Account, payee grid |
| `rib-direct-transfer.png` | Direct Transfer — Enter Fund Transfer Details (step 1 of 3 wizard) |
| `rib-pay-bills.png` | Payments (Pay Bills) — Saved Billers, biller categories |
| `rib-qr.png` | My QR Code — InstaPay receive-money QR |
| `rib-history.png` | Transaction History — account carousel + grouped transaction list |
| `rib-notifications.png` | Notifications — Transactions / Non Transactions tabs |
| `rib-profile.png` | My Profile — Personal Details / Preferences / Security Settings / Logout |

To re-explore the app and update this file, run Playwright against `https://ctbcqa.megalink.com.ph/web/`, enable Flutter accessibility (click the off-screen `flt-semantics-placeholder` "Enable accessibility" element), log in manually (OTP + Turnstile), and save new screenshots to `screenshots/rib-ui-exploration/`.

---

> Use this reference whenever writing test case steps for the RIB NetBanking app.
> All labels, button names, field names, and navigation paths below are **verified from the live UI**.

---

## 1. Login Page

**Route/title:** `Login` (URL: `https://ctbcqa.megalink.com.ph/web/`)
**Branding:** CTBC BANK logo + **NetBanking** wordmark
**Page heading:** Login

### Fields
| Field Label (placeholder) | Type |
|---|---|
| Enter your User ID | Text input |
| Enter your password | Password input (with show/hide eye toggle) |

### Links & Buttons
- `Forgot Password` link
- `User ID` link (forgot User ID) — rendered as "Forgot **Password** or **User ID**"
- **Cloudflare Turnstile** captcha widget (shows "Success!" once passed; has Privacy • Help links)
- `Login` button (teal, arrow icon)
- `Sign Up` button (outlined)

### Other elements
- Badges: PCI DSS certification, "A proud member of **BancNet**", **PDIC**
- Footer links: Privacy Policy · Security Statement · Terms and Conditions · FAQs
- Regulatory disclaimer: "CTBC Bank (Philippines) Corp. is regulated by the Bangko Sentral ng Pilipinas (BSP). • BSP Financial Consumer Protection Dept.: (02) 8708-7087 • consumeraffairs@bsp.gov.ph • https://www.bsp.gov.ph"
- "Deposits are insured by PDIC up to ₱1 Million per depositor."
- Version banner (top-left, diagonal): **1.1.974066**

### Post-login
- Login requires an **OTP / authenticator step** and passing the **Cloudflare Turnstile** challenge.
- A one-time **"Location Permission"** info dialog may appear on first load ("You can allow or deny location access when your browser asks. Allowing location enables additional security features...") with an `OK` button.

---

## 2. Global Layout (authenticated area)

Every authenticated screen shares this chrome:

### Left Navigation Sidebar
Icons with text labels (labels always visible at desktop width). Two groups:

**Top group**
| Item | Destination |
|---|---|
| **Home** | Dashboard (`/dashboard/home`) |
| **History** | Transaction History (`/dashboard/home/history`) |
| **Services** | Services screen |

**Bottom group**
| Item | Notes |
|---|---|
| **Settings** | Opens **My Profile** (`/dashboard/home/my-profile`) |
| **T&Cs** | Terms & Conditions |
| **Privacy Policy** | Privacy Policy |
| **FAQs** | Frequently Asked Questions |

### Top-right Header Icons
| Icon | Action |
|---|---|
| Notification bell (red count badge, e.g. "50") | Opens **Notifications** (`/dashboard/home/notification`) |
| Mail / message | Shows info dialog: **"This Feature will be made available."** with `OK` — **NOT YET IMPLEMENTED** in this build |
| Profile avatar | Opens **My Profile** (`/dashboard/home/my-profile`) |

### Right-side Help Card
A persistent card on the right of most screens: illustration + **"hello [First Name]"** + **"Need any assistance?"** link.

### Global footer / version
- **Version: 1.1.974066** shown on My Profile and as a top-left diagonal banner on every screen.

---

## 3. Dashboard

**Route/title:** `/dashboard/home`

### Greeting
- "Good Morning/Afternoon [First Name]!" heading
- "Welcome to your Dashboard" subtext
- Right side: "Last active" + timestamp (`MM/DD/YYYY hh:mm AM/PM`, e.g. `10/29/2026 04:56 PM`)

### Quick Actions (buttons)
| Button | Destination route |
|---|---|
| **My Accounts** | `/dashboard/home/my-products` |
| **Fund Transfer** | `/dashboard/home/send-money` |
| **Pay Bills** | `/dashboard/home/bill-payment` |
| **QR** | `/dashboard/home/qr` |

### Accounts Section
- Heading: **Accounts**
- Account-type tabs: **Savings** · **Time Deposits** · **Checking**
- Account cards, each showing:
  | Field | Example |
  |---|---|
  | Account type | Savings Account / Checking Account |
  | Balance | PHP 61,030.00 (currency code + space + amount with comma thousands + 2 decimals) |
  | (eye icon) | toggles balance visibility |
  | Nickname | Raymund G PEREZ |
  | Account Number | 001700062651 |

### Recent Transactions Section
- Heading: **Recent Transactions** with a count badge (e.g. "161")
- `See All` link → Transaction History (`/dashboard/home/history`)
- Table columns: **DATE** · **DESCRIPTION** · **ACCOUNT** · **AMOUNT**
- Amount shown in red for debits (e.g. `PHP103.00`)

### Promotions Section
- Heading: **Promotions** with a count badge
- Rotating promotional banner (e.g. "More deposits, more cash for your business.")

---

## 4. My Accounts

**Route/title:** `/dashboard/home/my-products`
**Page heading:** My Accounts

- `Filter ›` control
- `View All` link
- Account cards (one per account), each showing:
  | Field | Example |
  |---|---|
  | Account type | Savings Account / Checking Account |
  | Balance | PHP 61,030.00 |
  | (eye icon) | toggle balance visibility |
  | Nickname | Raymund G PEREZ |
  | Account Number | 001700062651 |
  | (chevron ›) | opens account detail |

Observed accounts for the test user: Savings (001700062651), Checking (001900012707), Savings (001700062700).

---

## 5. Fund Transfer

### 5.1 Fund Transfer Landing

**Route/title:** `/dashboard/home/send-money`
**Page heading:** Fund Transfer

- `Direct Transfer ›` button → `/dashboard/home/send-money-enter-transaction-details-for-direct-transfer`
- `Own Account ›` button (transfer between your own CTBC accounts)
- Tabs: **New Transfer** (active) · **View Schedule**
- `+ Add Payee` button
- **Saved payee grid** — each payee tile shows a network badge, nickname, and bank:
  - Network badges observed: **IN** (Instapay), **PE** (PESONET), **IN** (Intrabank/CTBC), **IV** (various)
  - Examples: "Instapay / PalawanPay", "PESONET / MARIBANK PHILIPPINES, INC.", "Intrabank / CTBC"

### 5.2 Direct Transfer — Enter Fund Transfer Details

**Route/title:** `/dashboard/home/send-money-enter-transaction-details-for-direct-transfer`
**Page heading:** Details

**Stepper (3 steps):** `1 Details` → `2 Review` → `3 Success`
**Section heading:** Enter Fund Transfer Details

#### Transfer From
- Account **carousel** (left/right arrows, dot indicators) showing source account card:
  - Currency (PHP), balance (e.g. 61,030.00), account-type badge (Savings Account), account holder name, account number

#### Transfer to
| Field | Type | Notes |
|---|---|---|
| Transfer destination toggle | Segmented buttons | **CTBC** / **Other Banks** |
| Currency Type | Dropdown | e.g. `PHP - PHP` |
| Amount | Text input | Validation message: "Amount cannot be empty" |
| (additional fields) | text / email inputs | e.g. recipient / email / remarks |

#### Buttons
- `Proceed Transfer`
- `Schedule this Transfer`
- `Reset`

---

## 6. Pay Bills (Payments)

**Route/title:** `/dashboard/home/bill-payment`
**Page heading:** Payments

- Section heading: **Saved Billers** with `View/Add` button
- Saved biller tiles (e.g. **Maynilad**)
- `Search` box
- Tabs: **New Payment** (active) · **Schedule Payment**
- **Biller category grid:**
  - Utilities
  - Credit Cards
  - Cash Card
  - Insurance
  - Loans
  - School
  - Donation
  - Others

---

## 7. QR (My QR Code)

**Route/title:** `/dashboard/home/qr`
**Page heading:** My QR Code

- `Select Bank Account` dropdown (e.g. "Raymund G PEREZ-001700062651")
- Instruction: **"Ask a friend to scan this QR code to send you money"**
- CTBC-branded **InstaPay** QR code image (receive money)

---

## 8. Transaction History

**Route/title:** `/dashboard/home/history`
**Page heading:** Transaction History
(Reached via sidebar **History** or dashboard **See All**.)

- Account **carousel** at top (left/right arrows + dot indicators) — selects which account's history is shown
- `Filter Transaction ›` link
- Transactions **grouped by date** (date chip e.g. `10/28/2026`, `10/23/2026`)
- Each transaction row shows:
  | Element | Example |
  |---|---|
  | Time | 10:17 AM |
  | Description | `OPHI 001  00151714 Sarah Duterte` |
  | Amount (signed) | `- PHP 103.00` (debit) / `+ PHP 1.00` (credit) |
  | (chevron ›) | opens transaction detail |

### Transaction description type codes observed
These prefixes appear in the DESCRIPTION field and indicate the transaction type/channel:
| Code | Meaning (inferred from context) |
|---|---|
| `OPHI` | Outgoing PhilPass / RTGS (e.g. "OPHI 001 ...") |
| `OPES` | Outgoing PESONET |
| `RBFT Intra` | Retail Banking Fund Transfer — Intrabank (CTBC-to-CTBC), ref `IFT...` |
| `RBIP IPY` | Retail Banking InstaPay, ref `IPY...` / `QRP2B...` / `QRP2M...` |
| `RBIP IPY Txn RVSL` | InstaPay transaction reversal (credit back) |
| `RBBP Bills PMT` | Retail Banking Bills Payment, ref `BP...` |
| `DWRT Withholding Tax` | Withholding tax debit |
| `CRIN` | Credit interest |

> Note: amounts use the format `PHP 103.00` (code + space + comma-grouped amount + 2 decimals). Debits are prefixed `-` and shown in red; credits are prefixed `+`.

---

## 9. Notifications

**Route/title:** `/dashboard/home/notification`
**Page heading:** Notifications
(Opened from the header notification bell.)

- Tabs: **Transactions** (active) · **Non Transactions**
- Filter dropdown: **All**
- `Clear All` button
- Notification cards, each with: info icon, **title**, message body, date (`YYYY/MM/DD`), and a dismiss (×) button.

### Example notification titles/bodies observed
- **"RTGS Fund Transfer Unsuccessful"** — "Your remittance of PHP 70.00 via RTGS/PhilPass to Joseph Estrada on OCT 28 2026 03:01:56 PM was unsuccessful with reason: BIC/National Id not found.. Txn ID: 00151753"
- **"RTGS Fund Transfer For Processing"** — "Your remittance of PHP 70.00 via RTGS/PhilPass to Joseph Estrada on OCT 28 2026 03:01:04 PM is subject for processing. Txn ID: 00151753."

---

## 10. My Profile

**Route/title:** `/dashboard/home/my-profile`
**Page heading:** My Profile
(Opened from the header profile avatar OR the sidebar **Settings** item.)

- User avatar, full name (e.g. "Raymund PEREZ")
- "Last active on: 10/29/2026 05:04 PM"
- Menu items (each a row with a trailing → arrow):
  - **Personal Details**
  - **Preferences**
  - **Security Settings**
  - **Logout**
- Footer: **Version: 1.1.974066**

---

## 11. Key UI Patterns (Global)

### Routes / page titles
Each screen writes its route into `document.title`, format `/dashboard/home[/sub-route]`. Verified routes:
`/dashboard/home` · `/dashboard/home/my-products` · `/dashboard/home/send-money` · `/dashboard/home/send-money-enter-transaction-details-for-direct-transfer` · `/dashboard/home/bill-payment` · `/dashboard/home/qr` · `/dashboard/home/history` · `/dashboard/home/notification` · `/dashboard/home/my-profile`

### Navigation
- In-screen **back arrow** (top-left of the content panel) returns to the previous screen.
- **Never** use browser Back/refresh — it logs the user out (`back_button_logout.js`).

### Currency format
- `PHP 61,030.00` — currency code + space + comma-grouped thousands + 2 decimals.
- In compact views amount may render without the space (e.g. `PHP103.00`).
- Debits: red text, `-` prefix. Credits: `+` prefix.

### Date / time format
- Date: `MM/DD/YYYY` (e.g. `10/29/2026`); notification dates use `YYYY/MM/DD`.
- Time: `hh:mm AM/PM`.

### Account display
- Account cards consistently show: type, balance (with eye toggle), Nickname, Account Number.

### Multi-step flows
- Transfers/payments use a numbered **stepper**: `1 Details → 2 Review → 3 Success`.

### Help card
- Persistent right-side "hello [First Name] / Need any assistance?" card on most authenticated screens.

---

## 12. Feature / Deployment Notes

| Feature | Screen | Status |
|---|---|---|
| Mail / Messages (header mail icon) | Global header | ⚠️ **NOT YET IMPLEMENTED** — shows dialog "This Feature will be made available." |
| Login | Login page | ✅ Live — requires OTP + Cloudflare Turnstile |
| Location Permission prompt | First load | ℹ️ Informational dialog (OK to dismiss) |

> These observations are from app version **1.1.974066** in the QA environment on October 29, 2026. Re-verify against the target environment's build before executing related test cases, since Flutter builds can change labels and routes between releases.

---

## 13. Automation Notes (for Playwright against this Flutter app)

Captured so future UI exploration is repeatable:
- The app lives at `https://ctbcqa.megalink.com.ph/web/`; all screens share this single URL (routing is client-side, surfaced in `document.title`).
- To read labels, **enable Flutter semantics** first by activating the off-screen element `flt-semantics-placeholder[aria-label="Enable accessibility"]` (click it via JS; it is 1px and off-viewport). After that, readable nodes appear as `flt-semantics` elements — use their `textContent` (not `aria-label`, which is usually empty).
- **Buttons** that expose `role="button"` in the semantics tree can be clicked reliably by clicking the element directly.
- **Sidebar nav icons** (History, Services) do **not** expose semantics and do **not** respond to synthetic coordinate clicks; reach those destinations via alternate in-app entry points (e.g. dashboard "See All" → History) or have a human click them.
- In-screen **back arrows** respond to coordinate clicks (top-left of the content panel, approx. x=318, y=99 at 1280×800).
- Do not call `page.goBack()` / `page.goto()` mid-session — it triggers logout.
