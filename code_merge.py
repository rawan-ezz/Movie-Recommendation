import os
import json

# this is two merge the two json files
base_path = "C:/Users/Admin/Desktop/SCRAPINGPROJECT/imdbscraper"
file1_path = os.path.join(base_path, "resulttwo.json")
file2_path = os.path.join(base_path, "resultone.json")
output_path = os.path.join(base_path, "final_merged_results.json")


if not os.path.exists(file1_path):
    print(f" File not found: {file1_path}")
    exit()

if not os.path.exists(file2_path):
    print(f" File not found: {file2_path}")
    exit()


with open(file1_path, 'r', encoding='utf-8') as f1:
    data1 = json.load(f1)

with open(file2_path, 'r', encoding='utf-8') as f2:
    data2 = json.load(f2)


data2_dict = {item['imdb_id']: item for item in data2}


merged_data = []
for item in data1:
    id = item.get('id')
    if id in data2_dict:
        merged_item = {**item, **data2_dict[id]}
        merged_data.append(merged_item)


with open(output_path, 'w', encoding='utf-8') as out:
    json.dump(merged_data, out, ensure_ascii=False, indent=2)

print(f"Merged data saved to: {output_path}")
