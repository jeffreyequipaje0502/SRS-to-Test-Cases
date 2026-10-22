# How to Use: SRS to Test Cases Skill

This skill reads your SRS document (PDF) and automatically generates a complete, ready-to-import test case Excel file for Azure DevOps.

---

## What You Need

- Your SRS document in **PDF format**
- Kiro IDE open with this workspace

---

## Steps

### 1. Open Kiro Chat

Click the Kiro chat panel on the side.

### 2. Attach Your SRS

**If your PDF is small (under ~10 pages):** drag and drop it into the chat.

**If your PDF is larger (~10+ pages):** convert it to text first to avoid an
API error with large attachments:

```
python scripts/pdf_to_text.py "path/to/your/SRS.pdf"
```

This creates a `.txt` file. Then in the chat, type `#` and select that `.txt`
file instead of dragging the PDF.

### 3. Type This Message

```
Generate test cases from this SRS
```

That's it. Hit send.

---

## What Kiro Will Do

1. Read and analyze the SRS document
2. Identify all features, user flows, rules, and edge cases
3. Generate test cases covering:
   - ✅ Normal / happy path scenarios
   - ❌ Error and negative scenarios
   - 🔲 Boundary / edge cases
   - 📋 Business rule validations
4. Save a ready-to-import Excel file in the `output/` folder
5. Give you a plain English summary of what was covered

---

## Your Output

**Excel file** → `output/<SRS_identifier>_TestCases.xlsx`

This file is already formatted for Azure DevOps import.  
No editing needed — just import it directly.

### How to Import to Azure DevOps

1. Go to **Azure DevOps → Test Plans**
2. Click **Import**
3. Select the Excel file from the `output/` folder
4. Done ✅

---

## Example

> You drag in `PHL-CTB-CIB-08-IB-Swift Charge_SRS_v1.3.pdf` and type:  
> *"Generate test cases from this SRS"*
>
> Kiro produces → `output/PHL-CTB-CIB-08-IB_SRS_v1.3_TestCases.xlsx`  
> with 100+ test cases, all steps filled in, ready to import.  
> Test case titles are prefixed with the actual feature name (e.g., "Transaction History", "FO Reports", "Swift Charge") — not the SRS filename.

---

## Notes

- The Excel generator script lives in `scripts/generate_testcases.py` — **do not delete it**
- Each run creates a new Excel file — previous ones are not overwritten
- If you want to re-run or tweak, the data script is saved in `output/<SRS_identifier>_data.py`
