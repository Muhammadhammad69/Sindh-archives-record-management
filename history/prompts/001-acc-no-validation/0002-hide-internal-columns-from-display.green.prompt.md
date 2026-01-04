---
id: 0002
title: Hide Internal Columns from Display
stage: green
date: 2026-01-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-acc-no-validation
branch: 001-acc-no-validation
user:
command: /sp.phr
labels: ["ui", "data-display", "security", "database", "streamlit"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - src/pages/commissioner_records.py
 - src/pages/court_records.py
 - test_internal_columns_removal.py
tests:
 - test_internal_columns_removal.py
---

## Prompt

# Remove Internal Columns from Record Display

## Prompt: Hide Internal Columns (id, created_at, updated_at) from Record Display Pages

Update the commissioner_records.py and court_records.py viewing pages to hide internal database columns (id, created_at, updated_at) from the public display. Users should only see the relevant business data columns, not the technical metadata fields. Modify the DataFrame display to exclude these columns before rendering with st.dataframe().

### Changes Required:

**File 1: src/pages/commissioner_records.py**

Locate the section where records are displayed (likely using st.dataframe or st.table). Modify it to exclude internal columns:

**Before:**
```python
# Current code probably looks like:
records = dao.get_all()
df = pd.DataFrame([record.__dict__ for record in records])
st.dataframe(df)  # Shows ALL columns including id, created_at, updated_at
```

**After:**
```python
# Get records from database
records = dao.get_all()

# Convert to DataFrame
df = pd.DataFrame([record.__dict__ for record in records])

# Remove internal columns - keep only business data
columns_to_display = [
    'acc_no',      # or 'Accession No.' depending on how it's labeled
    'department',
    'file_no',
    'subject',
    'year',
    'page',
    'condition',
    'record_type'
]

# Filter DataFrame to show only desired columns
df_display = df[columns_to_display]

# Rename columns for better display (optithe interface cleaner and more professional by hiding technical database metadata fields.

## Response snapshot

Successfully implemented the requested feature to hide internal columns (id, created_at, updated_at) from the record display pages. Modified both commissioner_records.py and court_records.py to remove internal columns before display while preserving all business data and functionality.

## Outcome

- ✅ Impact: Internal database columns (id, created_at, updated_at) are now hidden from user display in both commissioner and court record pages
- 🧪 Tests: Created and ran comprehensive test script to verify internal columns are properly removed while preserving business data
- 📁 Files: Modified src/pages/commissioner_records.py and src/pages/court_records.py to implement column filtering
- 🔁 Next prompts: none
- 🧠 Reflection: Using pandas drop() method with safety checks provides a robust way to remove internal columns while maintaining all existing functionality

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): All tests passed successfully
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none needed
