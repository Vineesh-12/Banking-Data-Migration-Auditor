# Banking Data Migration Auditor

An automated ETL auditing tool that scans migrated banking data for inconsistencies, extracts corrupted records, and generates analytical reports.

## Project Architecture

1. **SQL Backend**: T-SQL stored procedures actively hunt for data anomalies (e.g., negative balances, missing routing numbers) in the MS SQL database.
2. **.NET Engine**: A C# application acts as the orchestrator. It connects to the database, executes the audit procedures, and extracts bad data into a CSV format.
3. **Python Analyzer**: A Python script parses the output CSV to categorize the errors and generate a readable summary report.
4. **Automation**: A PowerShell script registers the .NET application with Windows Task Scheduler for daily automated runs.

## Folder Structure
- `database/`: SQL scripts for schema creation, mock data insertion, and audit logic.
- `src/`: C# source code for the .NET extraction engine.
- `scripts/`: Python analysis script and PowerShell automation script.

## Setup Instructions

1. **Database**
   - Run `database/schema.sql` to create the table.
   - Run `database/mock_data.sql` to populate some test data.
   - Run `database/sp_audit.sql` to create the stored procedure.

2. **Run the Audit**
   - Ensure you have the .NET 8 SDK installed.
   - Run the application:
     ```bash
     cd src
     dotnet run
     ```
   - This will extract `migration_errors.csv` and automatically trigger the Python script to create `audit_report.txt`.

3. **Schedule Automation**
   - Run `scripts/setup_scheduler.ps1` as Administrator to schedule the audit to run daily.
