import csv
from collections import Counter
from datetime import datetime
import os

def analyze_migration_errors(csv_file_path, output_report_path):
    print(f"Reading error log from: {csv_file_path}")
    
    if not os.path.exists(csv_file_path):
        print("Error: CSV file not found. Ensure Phase 3 has run successfully.")
        return

    error_counts = Counter()
    total_errors = 0
    accounts_affected = []

    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                total_errors += 1
                issue = row.get('IssueDescription', 'Unknown Error')
                error_counts[issue] += 1
                accounts_affected.append(row.get('AccountID', 'Unknown'))
                
        generate_report(output_report_path, total_errors, error_counts, accounts_affected)
        
    except Exception as e:
        print(f"Failed to analyze data: {e}")

def generate_report(output_path, total, counts, accounts):
    print("Generating summary report...")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("==================================================\n")
            f.write("        DATA MIGRATION AUDIT SUMMARY REPORT       \n")
            f.write("==================================================\n")
            f.write(f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("--- HIGH LEVEL METRICS ---\n")
            f.write(f"Total Corrupted Records Found: {total}\n\n")
            
            f.write("--- ERROR BREAKDOWN ---\n")
            for issue, count in counts.items():
                f.write(f"- {issue}: {count} instance(s)\n")
            
            f.write("\n--- AFFECTED ACCOUNTS ---\n")
            # Show up to 10 accounts to keep the report clean
            preview_accounts = accounts[:10]
            f.write(f"Account IDs: {', '.join(preview_accounts)}\n")
            if len(accounts) > 10:
                f.write(f"... and {len(accounts) - 10} more.\n")
                
            f.write("\n==================================================\n")
            f.write("End of Report\n")
            
        print(f"Report successfully saved to: {output_path}")
    except Exception as e:
        print(f"Failed to write report: {e}")

if __name__ == "__main__":
    # The C# app in Phase 3 outputs to the root directory
    csv_path = "../Phase3_Automation/migration_errors.csv" 
    # Fallback to local directory if run from root
    if not os.path.exists(csv_path):
         csv_path = "migration_errors.csv"
         
    report_path = "Audit_Report.txt"
    
    analyze_migration_errors(csv_path, report_path)
