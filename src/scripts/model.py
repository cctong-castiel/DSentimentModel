
import numpy as np
import regex as re

def cal_sentence_length(l_data, length=20):

    """to calculate the sentence length in l_data["post_message"]"""

    l_long = []
    l_short = []

    # loop l_data and check length
    for index, i in enumerate(l_data):
        if len(i["post_message"]) >= length:
            l_long.append(i)
        else:
            l_short.append(i)

    return l_long, l_short

def sent_remove_but_func(sent):

    """To remove sentences having 但 or 可是"""

    split_punc = re.split(r"[。!?]", sent)
    split_but = list(filter(lambda x: re.search("但|可是", x), split_punc))
    l_out = [re.split("但|可是", sent)[0] for sent in split_but]

    return l_out


def regex_sentiment(arr_, l_regex):

    """to run a regex sentiment on each sentences and determine sentiment"""

    def decide_sentiment(arr_sen):

        """To determine sentiment using arr_sen
           l_regex = [emoji_neg, emoji_pos, negative, neutral, positive"""

        pos = arr_sen[1] + arr_sen[4]
        neg = arr_sen[0] + arr_sen[2]
        neu = arr_sen[3]

        l_decision = [pos, neu, neg]
        if pos + neg + neu != 0:
            value = l_decision.index(max(l_decision))
        else:
            value = 1

        if value == 0:
            return 1
        elif value == 1:
            return 0
        else:
            return -1

    l_sen_out = []

    # remove but
    for sent in arr_:
        arr_sen = np.zeros(5)
        if re.search("但|可是", sent):
            split_b4_but = sent_remove_but_func(sent)
            # print(f"split_b4_but: \n {split_b4_but}")
            # print(f"sent: \n {sent}")
            j = "|".join(split_b4_but)

        for index, sen in enumerate(l_regex):
            cnt = len(re.findall(sen, sent))
            arr_sen[index] = cnt

        sen_value = decide_sentiment(arr_sen)

        l_sen_out.append(sen_value)

    return l_sen_out
