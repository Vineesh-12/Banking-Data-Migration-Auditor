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
    all_errors = []

    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                total_errors += 1
                issue = row.get('IssueDescription', 'Unknown Error')
                error_counts[issue] += 1
                all_errors.append(row)
                
        generate_html_report(output_report_path, total_errors, error_counts, all_errors)
        
    except Exception as e:
        print(f"failed to parse csv: {e}")

def generate_html_report(output_path, total, counts, all_errors):
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # Generate HTML rows for the table
    table_rows = ""
    for err in all_errors:
        table_rows += f"""
        <tr>
            <td>{err.get('AccountID', 'N/A')}</td>
            <td>{err.get('CustomerName', 'N/A')}</td>
            <td><span class="badge">{err.get('IssueDescription', 'N/A')}</span></td>
        </tr>
        """
        
    # Generate summary cards
    cards_html = ""
    for issue, count in counts.items():
        cards_html += f"""
        <div class="card">
            <h3>{count}</h3>
            <p>{issue}</p>
        </div>
        """

    # Modern Dark Mode HTML/CSS Template
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Migration Audit Dashboard</title>
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #3b82f6;
            --danger: #ef4444;
            --warning: #f59e0b;
        }}
        body {{
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 40px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            border-bottom: 1px solid #334155;
            padding-bottom: 20px;
        }}
        h1 {{
            font-size: 2.2rem;
            margin: 0;
            font-weight: 600;
        }}
        .timestamp {{
            color: var(--text-muted);
            font-size: 0.9rem;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .card {{
            background-color: var(--card-bg);
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #334155;
            transition: transform 0.2s;
        }}
        .card:hover {{
            transform: translateY(-3px);
        }}
        .card h3 {{
            font-size: 2.5rem;
            margin: 0 0 10px 0;
            color: var(--danger);
        }}
        .card p {{
            margin: 0;
            color: var(--text-muted);
            font-weight: 500;
        }}
        .table-container {{
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 24px;
            border: 1px solid #334155;
            overflow-x: auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}
        th, td {{
            padding: 16px;
            border-bottom: 1px solid #334155;
        }}
        th {{
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 0.05em;
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
        tr:hover td {{
            background-color: rgba(255,255,255,0.02);
        }}
        .badge {{
            background-color: rgba(239, 68, 68, 0.1);
            color: var(--danger);
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85rem;
            font-weight: 500;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>Data Migration Audit</h1>
                <p style="color: var(--text-muted); margin-top: 5px;">Q2 Platform Integration Dashboard</p>
            </div>
            <div class="timestamp">Generated: {date_str}</div>
        </div>

        <h2 style="margin-bottom: 20px; font-weight: 500;">Error Breakdown</h2>
        <div class="summary-grid">
            {cards_html}
        </div>

        <h2 style="margin-bottom: 20px; font-weight: 500;">Affected Accounts Log</h2>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Account ID</th>
                        <th>Customer Name</th>
                        <th>Identified Issue</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>"""

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"HTML Dashboard saved -> {output_path}")
    except Exception as e:
        print(f"failed to write html: {e}")

if __name__ == "__main__":
    csv_path = "../src/migration_errors.csv" 
    if not os.path.exists(csv_path):
         csv_path = "migration_errors.csv"
         
    # Generate HTML instead of TXT
    report_path = "audit_dashboard.html"
    analyze_migration_errors(csv_path, report_path)
