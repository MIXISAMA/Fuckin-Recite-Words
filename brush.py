from utils.my_config import MyConfig
from utils.wordlist import WordlistFactory
from utils.common import check_file_in_dir, traverse_dir
from utils import myio
from utils.myio import choose_one, my_input, my_print, fc, ready, print_a_b

config_path = "./config.cfg"
my_config = MyConfig(config_path)
myio.margin = my_config.margin


def print_wordlist_info(wordlist):
    ready()
    my_print(f"当前词库: {fc(wordlist['name'], 'yellow')}")
    my_print(f"单词量: {myio.fc(wordlist['size'], 'blue')}")
    my_print(f"总计背诵次数: {myio.fc(wordlist['frequency'], 'blue')}")

def change_wordlist():
    ready()
    wordlist_names = traverse_dir(my_config.wordlist_path)
    wordlist_name = wordlist_names[choose_one(wordlist_names)]
    my_config.default_wordlist_name = wordlist_name
    return WordlistFactory(my_config).open_by_wordlist(wordlist_name)

def change_group(wordlist):  
    option = []
    for i, group in enumerate(wordlist["groups"]):
        group_len = len(group)
        group_frequency = 0
        for head_word in group:
            group_frequency += wordlist["words"][head_word]["frequency"]
        option.append(f"共{fc(group_len, 'blue')}词 平均记忆频数:{fc(group_frequency/group_len, 'blue')}")
    print_wordlist_info(wordlist)
    wordlist.cur_group = wordlist["groups"][choose_one(option)]

def init():
    wordlist_names = set(traverse_dir(my_config.wordlist_path))
    wordlib_names = set(traverse_dir(my_config.wordlib_path))
    create_names = wordlib_names - wordlist_names
    for create_name in create_names:
        WordlistFactory(my_config).new_by_wordlib(create_name).save()

    wordlist_name = my_config.default_wordlist_name
    if wordlist_name not in (wordlist_names | wordlib_names):
        wordlist = change_wordlist()
    else:
        wordlist = WordlistFactory(my_config).open_by_wordlist(wordlist_name)

    change_group(wordlist)
    return wordlist

def show_head(wordlist):
    word = wordlist.cur_word
    ready()
    print_a_b(
        fc(word["headWord"], "yellow"),
        f"{fc(word['frequency'], 'blue')} {fc('★', 'yellow') if (word['headWord'] in wordlist['stars']) else '☆'}"
    )

def show_body(wordlist):
    word = wordlist.cur_word
    ready()
    print_a_b(
        fc(word["headWord"], "yellow"),
        f"{fc(word['frequency'], 'blue')} {fc('★', 'yellow') if (word['headWord'] in wordlist['stars']) else '☆'}"
    )
    print()
    content = word["content"]["word"]["content"]

    phone = content.get("phone")
    if my_config.country == "US":
        phone = content.get("usphone", phone)
    elif my_config.country == "UK":
        phone = content.get("ukphone", phone)
    my_print(fc(f"[{phone}]", "cyan"))

    for tran in content["trans"]:
        my_print(fc(tran["pos"]+".", "magenta"), fc(tran["tranCn"], "green"))
    
    rem = content.get("remMethod")
    if rem:
        my_print("记忆方法: ", fc(rem["val"], "cyan"))

def refresh(wordlist, answered):
    if answered:
        show_body(wordlist)
    else:
        show_head(wordlist)

def check_auto_save(init_freq, last_freq, cur_freq):
    return (cur_freq - init_freq) % 20 == 0 and not cur_freq == last_freq

def save(wordlist, delta_freq):
    wordlist.save()
    my_print(fc("已保存", "red"), fc(delta_freq, "blue"))


if __name__ == "__main__":
    ready()
    wordlist = init()
    init_freq = last_freq = wordlist["frequency"]

    wordlist.next_word()
    show_head(wordlist)
    answered = False

    while(True):

        if answered and check_auto_save(init_freq, last_freq, wordlist["frequency"]):
            save(wordlist, wordlist["frequency"]-init_freq)

        op = my_input()
        if op == "":            # 正常刷单词
            if answered:
                wordlist.next_word()
                show_head(wordlist)
                answered = False
            else:
                show_body(wordlist)
                answered = True
                wordlist.done()

        elif op == "'":         # 忘记该单词
            wordlist.forget()
            show_body(wordlist)
            if not answered:
                answered = True
                wordlist.done()

        elif op == "star":      # 加星
            wordlist.star()
            refresh(wordlist, answered)

        elif op == "unstar":    # 取消加星
            wordlist.unstar()
            refresh(wordlist, answered)

        elif op == "margin":    # 设置边距
            my_config.margin = myio.next_margin()
            refresh(wordlist, answered)
        
        elif op == "wordlist":  # 更换词库
            wordlist = change_wordlist()
            init_freq = last_freq = wordlist["frequency"]
            change_group(wordlist)
            wordlist.next_word()
            show_head(wordlist)
            answered = False

        elif op == "group":     # 更换组
            change_group(wordlist)
            if not answered:
                wordlist.cur_word = None
            wordlist.next_word()
            show_head(wordlist)
            answered = False
        
        elif op == "margin":
            myio.next_margin()
            refresh()
        
        elif op == ":w":                # 保存
            save(wordlist, wordlist["frequency"]-init_freq)

        elif op == ":x" or op == ":wq": # 保存退出
            save(wordlist, wordlist["frequency"]-init_freq)
            exit()

        elif op == ":q" or op == ":q!": # 不保存退出
            exit()
