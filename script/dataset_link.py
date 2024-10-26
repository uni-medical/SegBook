import csv
import requests
from bs4 import BeautifulSoup

# Step 1: Load Dataset Names from CSV
csv_file = 'static/data/STU_Benchmark_Information.csv'
datasets = []

with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) > 0:  # Ensure there's data in the row
            datasets.append(row[0])  # Assuming the first column contains the dataset names

# Step 2: Fetch and Parse Zhihu Article
zhihu_url = 'https://zhuanlan.zhihu.com/p/661132213'
response = requests.get(zhihu_url)
if response.status_code == 200:
    zhihu_content = response.text
else:
    raise Exception(f"Failed to fetch Zhihu page, status code: {response.status_code}")

soup = BeautifulSoup(zhihu_content, 'html.parser')

# Step 3: Search for Dataset Links in the Zhihu Article
dataset_links = {}
for dataset in datasets:
    if '_' in dataset:
        # Extract everything after the first underscore for matching
        english_name = dataset.split('_', 1)[1].lower().replace(' ', '')
        matching_link = None

        # Find all links in the Zhihu article
        links = soup.find_all('a', href=True)
        for link in links:
            link_text = link.get_text().strip().lower().replace(' ', '')
            # Debug: Print the dataset name and link text being compared
            print(f"Matching '{english_name}' with '{link_text}'")

            # If the link text contains the dataset name, save the link
            if english_name in link_text:
                matching_link = link['href']
                print(f"Found matching link: {matching_link}")
                break

        # Store the dataset link if found
        dataset_links[dataset] = matching_link if matching_link else '#'

# Step 4: Generate Updated HTML Code
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Datasets - SegBook</title>
    <link rel="stylesheet" href="static/css/styles.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap" rel="stylesheet">
    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdn.staticfile.org/font-awesome/4.7.0/css/font-awesome.css">
</head>
<body>
    <header>
        <!-- <h1>SegBook</h1>
        <p>Medical Segmentation CookBook</p> -->
    </header>
    <nav>
        <a href="index.html">Home</a>
        <a href="datasets.html">Datasets</a>
        <a href="leaderboard.html">Leaderboard</a>
        <a href="tools.html">Tools</a>
    </nav>
    <div class="container">
        <div class="section">
            <h2>Datasets</h2>
            <p>Our datasets include a variety of medical imaging data for training and evaluating segmentation models.</p>
            <div class="search-container">
                <input type="text" id="searchInput" placeholder="Search Datasets..." onkeyup="searchDatasets()">
            </div>
            <div class="datasets-grid" id="datasetsGrid">
                <!-- Dataset Boxes -->
                {dataset_boxes}
            </div>
        </div>
    </div>
    <script>
        function searchDatasets() {{
            const input = document.getElementById('searchInput').value.toLowerCase();
            const datasetBoxes = document.querySelectorAll('.dataset-box');
            datasetBoxes.forEach(box => {{
                const title = box.querySelector('h3').textContent.toLowerCase();
                if (title.includes(input)) {{
                    box.style.display = '';
                }} else {{
                    box.style.display = 'none';
                }}
            }});
        }}
    </script>
    <footer>
        <p>&copy; 2024 SegBook. All rights reserved.</p>
    </footer>
</body>
</html>
"""

dataset_boxes = ""

# Generate HTML for each dataset
for dataset in datasets:
    if '_' in dataset:
        english_name = dataset.split('_', 1)[1]
        link = dataset_links.get(dataset, '#')
        description = f"{english_name} Segmentation Dataset"
        dataset_box = f'''
        <div class="dataset-box">
            <h3>{dataset}</h3>
            <p>{description}</p>
            <a href="{link}" target="_blank">View Dataset</a>
        </div>
        '''
        dataset_boxes += dataset_box

# Step 5: Insert Dataset Boxes into HTML Template
html_content = html_template.format(dataset_boxes=dataset_boxes)

# Save the updated HTML file
with open('datasets_1.html', 'w', encoding='utf-8') as html_file:
    html_file.write(html_content)

print("Updated datasets.html generated successfully.")
