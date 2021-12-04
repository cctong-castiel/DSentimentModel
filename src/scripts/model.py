
import numpy as np
import regex as re
import logging
from math import log1p

def separate_sentence(l_data):

    """to separate object into 4 sentence generator"""

    arr_post = np.array([i["message"] for i in l_data])
    arr_id = np.array([i["live_sid"] for i in l_data])

    return arr_post, arr_id

def sent_remove_but_func(sent):

    """To remove sentences having 但 or 可是"""

    split_punc = re.split(r"[。!?]", sent)
    split_but = list(filter(lambda x: re.search("但|可是", x), split_punc))
    l_out = [re.split("但|可是", sent)[0] for sent in split_but]

    yield l_out

def regex_sentiment(arr_, l_regex):

    """to run a regex sentiment on each sentences and determine sentiment"""

    def decide_sentiment(arr_sen, xi=0.05):

        """To determine sentiment using arr_sen
            l_regex = [emoji_neg, emoji_pos, negative, neutral, positive]"""

        pos = arr_sen[1] + arr_sen[4]
        neg = arr_sen[0] + arr_sen[2]
        neu = arr_sen[3]

        # logging.info(f"emoji_neg: {arr_sen[0]}, emoji_pos: {arr_sen[1]}, neg: {arr_sen[2]}, neu: {arr_sen[3]}, pos: {arr_sen[4]}")
        score = log1p(pos + 0.5) - log1p(neg + 0.5)
        if score > 0 and neu > 0:
            score = score - neu * xi
        elif score < 0 and neu > 0:
            score = score + neu * xi

        yield score

    def calculate_score(sent):

        arr_sen = np.zeros(5)

         # remove but
        if re.search("但|可是", sent):
            split_b4_but = next(sent_remove_but_func(sent))
            logging.info(f"split_b4_but: \n {split_b4_but}")
            logging.info(f"sent: \n {sent}")
            sent = "|".join(split_b4_but)

        for index, sen in enumerate(l_regex):
            cnt = len(re.findall(sen, sent))
            arr_sen[index] = cnt

        sen_value = next(decide_sentiment(arr_sen))
        # logging.info(f"sen_value: {sen_value}")

        return sen_value

    l_sen_out = [calculate_score(sent) for sent in arr_]

    return l_sen_out

#########################################################################
# main pipeline
def sent_pipe(regex_config, p_data):

    """It is the default sentiment pipeline without using any modelling"""

    arr_post, arr_id = separate_sentence(p_data)

    arr_score = np.array(regex_sentiment(arr_post, regex_config))

    l_result = [{"live_sid": str(i), "pred": j, "post_message": str(k)} for i, j, k in zip(arr_id, arr_score, arr_post)]

    return l_result