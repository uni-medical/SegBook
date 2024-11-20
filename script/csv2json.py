import pandas as pd
import json
import os
import re

# Directory containing the CSV files
csv_directory = './static/data/result_segbook'

# Output directory for JSON files
output_directory = './static/data/json_segbook'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Dictionary to store the average values for each file
summary_data = {}

# Replacement mapping
replacement_mapping = {
    'nnunet': 'nn-UNet',
    'base': 'STU-Net-B',
    'large': 'STU-Net-L',
    'huge': 'STU-Net-H',
    'base_ft': 'STU-Net-B-ft',
    'large_ft': 'STU-Net-L-ft',
    'huge_ft': 'STU-Net-H-ft'
}

# Links for models
model_links = {
    'nn-UNet': 'https://github.com/MIC-DKFZ/nnUNet/tree/nnunetv1',
    'STU-Net-B': 'https://github.com/uni-medical/STU-Net',
    'STU-Net-L': 'https://github.com/uni-medical/STU-Net',
    'STU-Net-H': 'https://github.com/uni-medical/STU-Net',
    'STU-Net-B-ft': 'https://github.com/uni-medical/STU-Net',
    'STU-Net-L-ft': 'https://github.com/uni-medical/STU-Net',
    'STU-Net-H-ft': 'https://github.com/uni-medical/STU-Net'
}

# Loop through each CSV file in the directory
for csv_file in os.listdir(csv_directory):
    if csv_file.endswith('.csv'):
        # Read the CSV file
        file_path = os.path.join(csv_directory, csv_file)
        df = pd.read_csv(file_path)

        # Handle missing values by filling with 'NaN' (or any other strategy)
        df = df.fillna('NaN')

        # Remove Chinese characters from column names
        new_columns = [re.sub(r'--.*', '', col).strip() for col in df.columns]
        df.columns = new_columns

        # Replace elements in the first column based on the mapping
        df.iloc[:, 0] = df.iloc[:, 0].replace(replacement_mapping)

        # Calculate the average value for each row (ignoring the first column)
        df['Average'] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce').mean(axis=1).round(4)

        # Convert DataFrame to list of lists (for compatibility with the HTML display)
        data = [df.columns.tolist()] + df.astype(object).where(pd.notnull(df), 'NaN').values.tolist()

        # Add links to the model names
        for i in range(1, len(data)):
            model_name = data[i][0]
            if model_name in model_links:
                data[i][0] = {
                    "name": model_name,
                    "link": model_links[model_name]
                }

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
main_leaderboard = [['Evaluation'] + sorted(summary_data[next(iter(summary_data))].keys())]

for model_name, averages in summary_data.items():
    row = [model_name] + [round(averages.get(part, 0), 4) for part in main_leaderboard[0][1:]]
    if model_name in model_links:
        row[0] = {
            "name": model_name,
            "link": model_links[model_name]
        }
    main_leaderboard.append(row)

# Save the main leaderboard to a JSON file
main_output_path = os.path.join(output_directory, 'Main.json')
with open(main_output_path, 'w', encoding='utf-8') as f:
    json.dump(main_leaderboard, f, ensure_ascii=False, indent=4)

print("CSV files have been converted to JSON format successfully, and Main.json has been created.")
