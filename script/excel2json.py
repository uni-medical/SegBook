# convert_excel_to_json.py

import pandas as pd
import json

# Read the Excel file
excel_file = './static/data/Segbook_leaderboard.xlsx'  # Replace with your file name
xls = pd.ExcelFile(excel_file)

for sheet_name in xls.sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    # Convert DataFrame to list of lists
    data = [df.columns.tolist()] + df.values.tolist()
    # Save to JSON
    with open(f'static/data/{sheet_name}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
