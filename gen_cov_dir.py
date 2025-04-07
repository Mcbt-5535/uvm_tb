import os


def generate_test_list(root_path):
    tc_list = []
    # 遍历verif/testbench目录下的所有文件
    testbench_path = os.path.join(root_path, "verif", "testbench", "tests")
    # 查找所有your_dut_name_agent目录
    for testcase in os.listdir(testbench_path):
        if testcase.endswith(('.sv', '.svh')):
            testcase_name = os.path.splitext(testcase)[0]
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

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir)
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
    pretty_print_dict(tc_dict)
