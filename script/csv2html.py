import csv

# 输入 CSV 文件的路径
csv_file_path = "static/data/dataset_detailed_info.csv"
# 输出 HTML 文件的路径
output_html_path = "static/data/datasets_generated.html"

# 读取 CSV 文件并生成 HTML 代码块
html_code = ""
with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')  # 使用逗号作为分隔符
    # print(reader.fieldnames)
    for row in reader:
        display_name = row['展示数据集名字']
        chinese_link = row['中文链接']
        english_link = row['英文链接']
        homepage_link = row['数据集主页']
        
        html_code += f"""
        <div class="dataset-box">
            <h3>{display_name}</h3>
            <a href="{chinese_link}" target="_blank">View Dataset (Chinese)</a><br>
            <a href="{english_link}" target="_blank">View Dataset (English)</a><br>
            <a href="{homepage_link}" target="_blank">Dataset Homepage</a>
        </div>
        """

# 保存生成的 HTML 代码到文件
with open(output_html_path, 'w', encoding='utf-8') as output_file:
    output_file.write(html_code)

print(f"HTML code saved to {output_html_path}")
