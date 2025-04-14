import os
import argparse

DEFAULT_ROUND = 5
IGNORE_LIST = ["base_test"]


def generate_test_list(root_path):
    tc_list = []
    # 遍历verif/testbench目录下的所有文件
    testbench_path = os.path.join(root_path, "verif", "testbench", "tests")
    # 查找所有your_dut_name_agent目录
    for testcase in os.listdir(testbench_path):
        if testcase.endswith(('.sv', '.svh')):
            testcase_name = os.path.splitext(testcase)[0]
            if testcase_name in IGNORE_LIST:
                continue
            tc_list.append(testcase_name)
    return tc_list


def pretty_print_dict(d):
    print("{")
    for key, values in d.items():
        print(f'    "{key}": [')
        for value in values:
            print(f'        "{value}"{"," if value != values[-1] else ""}')
        print("    ]" + ("," if key != list(d.keys())[-1] else ""))
    print("}")


def save_dict_to_file(dictionary, file_path):
    """
    将字典保存到文件中。如果已经存在则不覆盖
    """
    if os.path.exists(file_path):
        print(f"file {file_path} exists, skip")
        return
    with open(file_path, 'w', encoding='utf-8') as file:
        for key, values in dictionary.items():
            for value in values:
                file.write(f'{key}: {value}, {DEFAULT_ROUND},\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--output_path", type=str, required=True)
    # args = parser.parse_args()
    # output_path = args.output_path
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test.txt"))
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, "auto_tb")
    test_folders = []
    tc_dict = {}
    # 遍历文件夹a中的所有条目
    for entry in os.listdir(folder_path):
        full_path = os.path.join(folder_path, entry)
        # 检查是否是文件夹且以_dv结尾
        if os.path.isdir(full_path) and entry.endswith('_dv'):
            test_folders.append(full_path)
            tc_list = generate_test_list(full_path)
            tc_dict[entry[:-3]] = tc_list

    # 打印所有待测ip下的测试用例
    # pretty_print_dict(tc_dict)
    save_dict_to_file(tc_dict, output_path)
