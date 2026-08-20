# Banking Data Migration Auditor

This project is an **Automated Data Migration Audit Tool** designed to scan a banking database for data corruption (migration errors), export those errors, and use Python to analyze what went wrong.

This directly aligns with the responsibilities of troubleshooting and resolving customer data migration problems in a Fintech environment.

## Tech Stack
*   **MS SQL / T-SQL:** For database storage and advanced error identification logic.
*   **.NET (C#):** For automation, orchestration, and extracting the corrupted records.
*   **Python:** For performing data analysis on the extracted error logs.

## Phases

*   [x] **Phase 1:** Environment Setup & Mock Data Creation (MS SQL)
*   [x] **Phase 2:** Database Logic & Error Identification (T-SQL)
*   [ ] **Phase 3:** Automation & Extraction (.NET)
*   [ ] **Phase 4:** Data Analysis & Reporting (Python)
*   [ ] **Phase 5:** Final Integration & Scheduling

## Phase 1: Setup Instructions

1.  Open SQL Server Management Studio (SSMS).
2.  Execute `Phase1_DatabaseSetup/01_Create_Schema.sql` to create the database and table.
3.  Execute `Phase1_DatabaseSetup/02_Insert_MockData.sql` to populate the table with dummy data (which intentionally includes migration errors).
