import os
import sys

platform = sys.platform
cls_cmd = 'cls' if platform.startswith('win') else 'clear'

front_color = {
    'red': '31m',
    'green': '32m',
    'yellow': '33m',
    'blue': '34m',
    'magenta': '35m',
    'cyan': '36m',
}
back_color = {
    'red': '41m',
    'green': '42m',
    'yellow': '43m',
    'blue': '44m',
    'magenta': '45m',
    'cyan': '46m',
}

margin = 1/3

def next_margin():
    global margin
    if margin < 1/6:    # 0 -> 1/5
        margin = 1/5
    elif margin < 1/4:  # 1/5 -> 1/3
        margin = 1/3
    else:               # 1/3 -> 0
        margin = 0
    return margin

def _blanks():
    sz = os.get_terminal_size()
    max_cols = sz.columns
    return int(max_cols * margin)

def my_print(*args, **kwargs):
    print(" "*_blanks(), end="")
    print(*args, **kwargs)

def my_input(*args, **kwargs):
    print(" "*(_blanks()-2)+">>", end="")
    return input(*args, **kwargs)

def ready():
    os.system(cls_cmd)
    sz = os.get_terminal_size()
    max_rows = sz.lines
    start_row = int(max_rows * margin)
    for i in range(start_row):
        print()

def print_a_b(a, b):
    """a靠左边。如果可能，b靠右边"""
    len_a = len(a) - a.count("\033") // 2 * 11
    len_b = len(b) - b.count("\033") // 2 * 11
    max_cols = os.get_terminal_size().columns
    blanks = int(max_cols * margin)
    sep = max_cols - 2*blanks - len_a - len_b
    if platform.startswith('win'):
        sep -= 1
    print(" "*blanks, end="")
    print(a, b, sep=" "*sep)

def fc(s, color):
    """给字符串s只加前景色color效果"""
    return f"\033[0;{front_color[color]}{s}\033[0m"

def bc(s, color):
    """给字符串s只加背景色color效果"""
    return f"\033[0;0;{back_color[color]}{s}\033[0m"

def choose_one(options):
    """
    在options字符串数组中挑选一个
    input输入挑选序号
    """
    size = len(options)
    while True:
        my_print(f"从以下 { fc(size, 'blue') } 项中选择一项")
        for i, option in enumerate(options):
            my_print(f" { fc(f'[{i+1}]', 'magenta') :4} :  {option}")
        try:
            index = int(my_input())
            if 1 <= index <= size:
                return index - 1
        except ValueError:
            pass
