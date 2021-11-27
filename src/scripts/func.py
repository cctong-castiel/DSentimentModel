# coding=utf-8
# func.py

import logging
import glob
import regex as re


def prepare_config():

    """To prepare emoji and sentiment words config"""

    # a list of config.txt
    l_txt = sorted(glob.glob("./config/*.txt"))
    print(f"l_txt: {l_txt}")

    l_config = []
    for index, path in enumerate(l_txt):
        with open(path, "r") as f:
            l_ = f.read().splitlines()
        str_sen = "|".join(l_)
        sen_regex = re.compile(str_sen)
        l_config.append(sen_regex)

    return l_config
