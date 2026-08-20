import csv
from collections import Counter
from datetime import datetime
import os

def analyze_migration_errors(csv_file_path, output_report_path):
    print(f"Reading: {csv_file_path}")
    
    if not os.path.exists(csv_file_path):
        print("err: csv not found")
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
        print(f"failed to parse csv: {e}")

def generate_report(output_path, total, counts, accounts):
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Data Migration Audit - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total Corrupted Records: {total}\n\n")
            
            f.write("Breakdown:\n")
            for issue, count in counts.items():
                f.write(f"- {issue}: {count}\n")
            
            f.write("\nAffected Accounts (Sample):\n")
            preview = accounts[:10]
            f.write(f"{', '.join(preview)}\n")
            if len(accounts) > 10:
                f.write(f"... and {len(accounts) - 10} more.\n")
            
        print(f"Report saved -> {output_path}")
    except Exception as e:
        print(f"failed to write report: {e}")

if __name__ == "__main__":
    csv_path = "../src/migration_errors.csv" 
    if not os.path.exists(csv_path):
         csv_path = "migration_errors.csv"
         
    report_path = "audit_report.txt"
    analyze_migration_errors(csv_path, report_path)
