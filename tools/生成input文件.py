import os
from tqdm import tqdm

root = '/45TB/xx/CMLRdataset/text'
file_list = []


def traverse_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in tqdm(files, total=len(files), desc=f'{root}/{dirs}生成中'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf8') as F:
                content = F.readline()
                file_list.append(content)
            F.close()


traverse_files(root)
output_file = '../spm/input_zh.txt'
with open(output_file, 'w', encoding='utf8') as f:
    f.writelines(file_list)
f.close()
print(file_list[0])
