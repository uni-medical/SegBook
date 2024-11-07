# convert_csv_to_json.py

import pandas as pd
import json
import os
import re

# Directory containing the CSV files
csv_directory = './static/data/result_segbook'

# Output directory for JSON files
output_directory = './static/data/json_segbook'

# Dictionary to store the average values for each file
summary_data = {}

# Loop through each CSV file in the directory
for csv_file in os.listdir(csv_directory):
    if csv_file.endswith('.csv'):
        # Read the CSV file
        file_path = os.path.join(csv_directory, csv_file)
        df = pd.read_csv(file_path)
        
        # Remove Chinese characters from column names
        new_columns = [re.sub(r'--.*', '', col).strip() for col in df.columns]
        df.columns = new_columns
        
        # Calculate the average value for each row (ignoring the first column)
        # 小数点保留4位数
        df['Average'] = df.iloc[:, 1:].mean(axis=1).round(4)
        
        # Convert DataFrame to list of lists (for compatibility with the HTML display)
        data = [df.columns.tolist()] + df.values.tolist()
        
        # Construct JSON file name from CSV name
        json_file_name = os.path.splitext(csv_file)[0] + '.json'
        output_path = os.path.join(output_directory, json_file_name)
        
        # Save to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        # Add the average values to the summary data for the main leaderboard
        json_name = os.path.splitext(csv_file)[0]  # Use the JSON name (body part name)
        for index, row in df.iterrows():
            model_name = row[df.columns[0]]
            average_value = row['Average']
            if model_name not in summary_data:
                summary_data[model_name] = {}
            summary_data[model_name][json_name] = average_value

# Prepare the main leaderboard data based on averages
main_leaderboard = [['Evaluation'] + list(summary_data[next(iter(summary_data))].keys())]

for model_name, averages in summary_data.items():
    row = [model_name] + [round(averages[part], 4) for part in main_leaderboard[0][1:]]
    main_leaderboard.append(row)

# Save the main leaderboard to a JSON file
main_output_path = os.path.join(output_directory, 'Main.json')
with open(main_output_path, 'w', encoding='utf-8') as f:
    json.dump(main_leaderboard, f, ensure_ascii=False, indent=4)

print("CSV files have been converted to JSON format successfully, and Main.json has been created.")
