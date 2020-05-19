from collections import UserDict
from random import shuffle, sample, random
import pickle
import json

from .common import round_up

class WordlistFactory:

    def __init__(self, my_config):
        self._my_config = my_config

    def new_by_wordlib(self, wordlist_name):
        wordlist = {
            "wordlist_path": self._my_config.wordlist_path,
            "name": wordlist_name,
            "size": 0,
            "frequency": 0,
            "words": {},
            "groups": [],
            "forgotten": [],
            "stars": set(),
        }
        with open(self._my_config.wordlib_path+wordlist_name+'.json', 'r', encoding='UTF-8') as f:
            words = [json.loads(line) for line in f.readlines()]
            shuffle(words)
            
        wordlist["words"] = dict([(word["headWord"], word) for word in words])
        wordlist["size"] = len(wordlist["words"])
        max_number = self._my_config.max_number
        groups_number = round_up(wordlist["size"], max_number)
        rest_words_number = wordlist["size"] # 剩余单词数量
        for i in range(groups_number):
            rest_groups_number = groups_number - i # 剩余组数量
            words_number = round_up(rest_words_number, rest_groups_number) # 本组单词数量
            words_in_this_group = set()
            start = wordlist["size"] - rest_words_number
            rest_words_number -= words_number
            for word in words[start: start+words_number]:
                word["frequency"] = 0
                word_head = word["headWord"]
                words_in_this_group.add(word_head)
                wordlist["words"][word_head] = word
            wordlist["groups"].append(words_in_this_group)
        return Wordlist(wordlist)

    def open_by_wordlist(self, wordlist_name):
        with open(self._my_config.wordlist_path+wordlist_name, 'rb') as f:
            return Wordlist(pickle.load(f))

class Wordlist(UserDict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cur_group = None
        self.cur_word = None
    
    def done(self):
        if self.cur_word is not None:
            self.cur_word["frequency"] += 1
            self["frequency"] += 1

    def next_word(self):
        if self.cur_group is None:
            return None

        if random() < 0.1 and self["forgotten"]:      # 1/10概率下一个单词为忘记单词
            self.cur_word = self["words"][sample(self["forgotten"], 1)[0]]
        elif random() < 0.1 and self["stars"]:        # 1/10概率下一个单词为加星单词
            self.cur_word = self["words"][sample(self["stars"], 1)[0]]
        else:
            self.cur_word = self["words"][sample(self.cur_group, 1)[0]]
    
    def forget(self):
        self["forgotten"].append(self.cur_word["headWord"])
        if self.cur_word["frequency"] >= 5:
            self.star()

    def star(self):
        self["stars"].add(self.cur_word["headWord"])

    def unstar(self):
        self["stars"].discard(self.cur_word["headWord"])

    def save(self):
        with open(self["wordlist_path"]+self["name"], "wb") as f:
            pickle.dump(self, f)
