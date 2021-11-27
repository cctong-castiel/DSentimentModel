import numpy as np
import regex as re
import emoji
import multiprocessing as mp

class AdRemover():

    """It is a class for classifying a post is ad or non-ad"""

    l_emoji = list(map(lambda x: "".join(x.split()), emoji.UNICODE_EMOJI.keys()))

    var = {
        "slashN": re.compile(r"\n\n"),
        "hashtag": re.compile(r"#"),
        "stock": re.compile(r"\(\d+\)"),
        "tel": re.compile(r"(852)*\d{8}\s"),
        "digit": re.compile(r"\d+"),
        "emoji": re.compile(r"\b(%s)\b" % "|".join(re.escape(p) for p in l_emoji)),
        "line": re.compile(r"\b(———+|▬▬▬▬+|====+|\+\+\+\+\+\+\+\+|『|』|《|》|（|）|：)\b"),
        "link": re.compile(r"https*://"),
        "star": re.compile(r"\*"),
        "punc": re.compile(r"[。！?]"),
        "threshold1": [0.0, 3.0, 0.0, 0.0, 28.75, 1.0, 0.0, 3.5, 5],
        "threshold2": [0.0],
        "filter": [1.1, 1.1, 1, 1, 1, 1, 1, 1, 1, 1]
    }

    def __init__(self, arr):

        self.arr = arr

    def regex_item(self, regex):
        return np.array(list(map(lambda x: len(regex.findall(x)), self.arr)))

    @property
    def fit(self):

        # multiprocessing
        cpu = mp.cpu_count() - 1
        p = mp.Pool(cpu)

        l_regex_item2 = p.map(self.regex_item, [self.var["slashN"],
                                              self.var["hashtag"],
                                              self.var["stock"],
                                              self.var["tel"],
                                              self.var["digit"],
                                              self.var["emoji"],
                                              self.var["line"],
                                              self.var["link"],
                                              self.var["star"],
                                              self.var["punc"]])

        arr_out1 = np.array(
            np.column_stack(
                (l_regex_item2[0],
                l_regex_item2[1],
                l_regex_item2[2],
                l_regex_item2[3],
                l_regex_item2[4],
                l_regex_item2[5],
                l_regex_item2[6],
                l_regex_item2[7],
                l_regex_item2[8])
            )
        )


        arr_out2 = np.reshape(l_regex_item2[9], (-1, 1))

        '''
        start_time2 = time.time()
        arr_out1 = np.array(list(zip(*[
            list(map(lambda x: x.count(self.var["slashN"]), self.arr)),
            list(map(lambda x: x.count(self.var["hashtag"]), self.arr)),
            list(map(lambda x: len(self.var["stock"].findall(x)), self.arr)),
            list(map(lambda x: len(self.var["tel"].findall(x)), self.arr)),
            list(map(lambda x: len(self.var["digit"].findall(x)), self.arr)),
            list(map(lambda x: len(self.var["emoji"].findall(x)), self.arr)),
            list(map(lambda x: len(self.var["line"].findall(x)), self.arr)),
            list(map(lambda x: len(self.var["link"].findall(x)), self.arr)),
            list(map(lambda x: x.count(self.var["star"]), self.arr))
        ])))

        arr_out2 = np.array(list(zip(*[
            list(map(lambda x: len(self.var["punc"].findall(x)), self.arr))
        ])))'''

        p.close()
        p.join()

        return arr_out1, arr_out2

    def transform(self, arr1, arr2):

        # array of thresholds
        arr_up_con = np.where(arr1 > self.var["threshold1"], 1, 0)
        arr_down_con = np.where(arr2 < self.var["threshold2"], 1, 0)

        # horizontal stack
        arr_con = np.hstack((arr_up_con, arr_down_con))

        # calculate weighted value array
        arr_con2 = arr_con * self.var["filter"]
        arr_cutoff = arr_con2.sum(axis=1)

        # generate ad cutoff
        arr_ad = np.array([1 if i > 1 else 0 for i in arr_cutoff], dtype=bool)

        return arr_ad
