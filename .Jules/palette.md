## 2026-10-13 - Empty state for case lists
**Learning:** For CLI tools that present tabular data, rendering an empty table when no data exists can be confusing. Adding an actionable empty state panel (using `rich.panel.Panel` in Python) is an effective and easy UX win that provides clear guidance on the next steps (e.g. how to create the missing resource).
**Action:** Always check if a list/query is empty before rendering it into a table and display an actionable "empty state" panel instead.
