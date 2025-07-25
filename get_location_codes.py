import json
import re
import pandas as pd

def extract_foreign_countries():
    # 从Estero.txt文件中提取外国代码
    countries = []
    with open('location_estero.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳过空行
            if not line:
                continue
            # 使用正则表达式匹配代码和国家名称
            match = re.match(r'Z(\d+)\s+(.+)', line)
            if match:
                code = 'Z' + match.group(1)
                name = match.group(2).strip()
                # 排除包含 = 的行，因为这些通常是别名
                if '=' not in name:
                    countries.append({
                        "code": code,
                        "type": "Estero",
                        "name": name,
                    })
    return countries

def extract_comuni():
    # 从Excel文件中提取城市代码
    df = pd.read_excel('location_comuni.xlsx')

    comuni = []
    for _, row in df.iterrows():
        try:
            # 使用新的列名
            code = row['Codice catastale del comune']
            name = row['Comune (provincia)']
            
            # 去除括号中的省份信息
            name = re.sub(r'\s*\([^)]*\)', '', name).strip()
            
            comuni.append({
                "code": code,
                "type": "Comune",
                "name": name,
            })
        except KeyError as e:
            print(f'警告: 找不到必要的列: {e}')
            continue
    
    return comuni

def merge_location_codes():
    # 获取两个数据源的数据
    foreign_countries = extract_foreign_countries()
    comuni = extract_comuni()
    
    # 按类型分组数据
    grouped_locations = {
        "Comune": [{
            "code": item["code"],
            "name": item["name"]
        } for item in comuni],
        "Estero": [{
            "code": item["code"],
            "name": item["name"]
        } for item in foreign_countries]
    }
    
    # 对每个类型内的数据按代码排序
    for location_type in grouped_locations:
        grouped_locations[location_type].sort(key=lambda x: x['code'])
    
    # 将结果保存为JSON文件
    with open('location_codes.json', 'w', encoding='utf-8') as f:
        json.dump(grouped_locations, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    merge_location_codes()