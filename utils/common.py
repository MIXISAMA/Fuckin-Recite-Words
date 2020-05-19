import os

def round_up(a: int, b: int):
    """a除以b 并向上取整"""
    return (a + b - 1) // b

def traverse_dir(dir_path):
    """遍历lib文件夹，获取所有文件名"""
    # if len(files_info) == 0:
    #     print(bc("无词库", "red"), "请从此仓库添加词库")
    #     print("https://github.com/kajweb/dict")
    #     exit()
    return [file_name.split(".json")[0] for file_name in os.listdir(dir_path)]

def check_file_in_dir(file_name, dir_path):
    return file_name in traverse_dir(dir_path)