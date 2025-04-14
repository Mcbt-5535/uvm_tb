def load_dict_from_file(filename):
    """
    从文件读取并还原字典结构
    支持格式：key:value,number,
    忽略以 # 开头的注释行
    """
    restored_dict = {}

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            # 清理行内容
            line = line.strip()

            # 跳过空行和注释行
            if not line or line.startswith('#'):
                continue

            # 去除行尾逗号（可能有多个）
            while line.endswith(','):
                line = line[:-1]

           
            # 分割键和值部分
            key_part, value_part = line.split(':', 1)
            key = key_part.strip()

            # 分割值和数字
            value_str, num_str = value_part.split(',', 1)
            value = value_str.strip()
            num = int(num_str.strip())

           
            # 保存到字典
            if key in restored_dict:
                restored_dict[key].append((value, num))
            else:
                restored_dict[key] = [(value, num)]

    return restored_dict


if __name__ == "__main__":
    try:
        dict_restored = load_dict_from_file('test.txt')
        print(dict_restored)
        print("从文件还原的字典：")
        for k, v in dict_restored.items():
            print(f"{k}: {v}")
    except FileNotFoundError:
        print("错误: test.txt 文件不存在")
