from preparation.transforms import TextTransform
import csv

textTrans = TextTransform()  # 分词器转换
for subset in ['train','test','val']:
    input_path = f'/45TB/xx/CMLRdataset/{subset}.csv'

    filename_list = []
    with open(input_path, 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            filename_list.append(row)
    f.close()

    # 输出保存的label文件--Dataset读取的文件
    output_savePath = f'{subset}.csv'

    root = 'video'
    lines_list = []
    # 读取每行所需的四部分信息
    for filename in filename_list:
        filepath = '/45TB/xx/CMLRdataset/text/' + filename[0].replace('_', '/', 1) + '.txt'
        with open(filepath, 'r', encoding='utf8') as f:
            txt = f.readline().strip()
        f.close()
        rel_path = filename[0].replace('_', '/', 1) + '.mp4'
        length = len(txt)
        tokenID = textTrans.tokenize(txt)
        tokenID_str = ' '.join([str(i) for i in tokenID])
        lines_list.append([root, rel_path, str(length), tokenID_str])
        # lines_list.append(','.join([root, rel_path, str(length), tokenID_str + '\n']))

    # 写入文本
    with open(output_savePath, 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        for line in lines_list:
            writer.writerow(line)
    f.close()
