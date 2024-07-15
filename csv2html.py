import pandas as pd

# 读取CSV文件
csv_path = 'gmai/SegBook/static/data/dataset_result.csv'
df = pd.read_csv(csv_path)

# 获取所有唯一的模态
modalities = set()
for modalities_str in df['Modality MR Sequence'].dropna():
    modalities.update(modalities_str.split(','))

# 开始生成HTML
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Leaderboard - SegBook</title>
    <link rel="stylesheet" href="https://cdn.staticfile.org/font-awesome/4.7.0/css/font-awesome.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        header {
            background-color: #333;
            color: white;
            padding: 10px 0;
            text-align: center;
        }
        nav {
            display: flex;
            justify-content: center;
            background-color: #444;
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 1000;
        }
        nav a {
            color: white;
            padding: 14px 20px;
            text-decoration: none;
            text-align: center;
        }
        nav a:hover {
            background-color: #555;
        }
        .container {
            padding: 20px;
            padding-top: 80px; /* Offset for fixed navbar */
        }
        .section {
            background-color: white;
            margin: 20px 0;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .section h2 {
            margin-top: 0;
        }
        .filter-container {
            margin-bottom: 20px;
        }
        .filter-container select {
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        .table-container {
            max-height: 600px; /* Adjust this value as needed */
            overflow-y: auto;
            overflow-x: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        th, td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: center;
        }
        th {
            background-color: #f4f4f4;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
        footer {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 18px 0;
        }
        footer p {
            margin: 0;
        }
    </style>
</head>
<body>
    <header>
        <h1>SegBook</h1>
        <p>Medical Segmentation CookBook</p>
    </header>
    <nav>
        <a href="index.html">Home</a>
        <a href="datasets.html">Datasets</a>
        <a href="leaderboard.html">Leaderboard</a>
        <a href="tools.html">Tools</a>
    </nav>
    <div class="container">
        <div class="section">
            <h2>Leaderboard</h2>
            <div class="filter-container">
                <label for="modalityFilter">Filter by Modality:</label>
                <select id="modalityFilter" onchange="filterTable()">
                    <option value="">All</option>
'''

# 添加筛选选项
for modality in sorted(modalities):
    html_content += f'<option value="{modality.strip()}">{modality.strip()}</option>\n'

html_content += '''
                </select>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Index</th>
                            <th>Source dataset</th>
                            <th>Modality MR Sequence</th>
                            <th>Is totalseg</th>
                            <th>Is structure</th>
                            <th>Is lesion</th>
                            <th>Train cases</th>
                            <th>Dice nnunet</th>
                            <th>Dice base</th>
                            <th>Dice base_ft</th>
                            <th>Dice large</th>
                            <th>Dice large_ft</th>
                            <th>Dice huge</th>
                            <th>Dice huge_ft</th>
                            <th>Modality</th>
                            <th>Total case</th>
                            <th>benefit_base_ft</th>
                            <th>benefit_large_ft</th>
                            <th>benefit_huge_ft</th>
                        </tr>
                    </thead>
                    <tbody>
'''

# 生成表格数据行
for _, row in df.iterrows():
    html_content += '<tr>'
    for value in row:
        html_content += f'<td>{value}</td>'
    html_content += '</tr>\n'

# 结束HTML
html_content += '''
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <script>
        function filterTable() {
            const filter = document.querySelector('#modalityFilter').value.toLowerCase();
            const rows = document.querySelectorAll('tbody tr');

            rows.forEach(row => {
                const modalityCell = row.querySelector('td:nth-child(3)');
                if (modalityCell) {
                    const modalityText = modalityCell.textContent.toLowerCase();
                    if (filter === '' || modalityText.includes(filter)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                }
            });
        }
    </script>
</body>
</html>
'''

# 将HTML内容写入文件
with open('/Users/yanjunli/codefield/python/gmai/SegBook/leaderboard.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

print("HTML 文件已生成")