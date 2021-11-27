# main.py

# mods
import os
import json
import logging
import shutil
import gc
import time
import numpy as np
from dotenv import load_dotenv
from sanic import Sanic
from sanic.response import json as Json, text
from scripts.adFeatures import AdRemover
from scripts.func import prepare_config
from scripts.model import *


# app
app = Sanic(__name__)

# log
logger = logging.getLogger(__name__)
logging.basicConfig(filename="./log/dsent.log", filemode="a", level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# route
@app.route("/ping", methods=["GET"])
async def home(request):
    ret = "pong"
    return text(ret)

@app.route("/run", methods=["POST"])
async def run(request):

    # post request
    data = request.json
    p_data = data["p_data"]
    p_data = [{"post_message": i, "live_sid": j} for i, j in zip(p_data["post_message"], p_data["live_sid"])]
    print(f"length of p_data: {len(p_data)}")

    # prepare config
    # emoji_neg, emoji_pos, negative, neutral, positive
    logging.info("prepare config")
    l_regex = prepare_config()

    # separate 2 lists(long sentence and short sentence)
    logging.info("separate 2 lists")
    l_long, l_short = cal_sentence_length(p_data, length=20)
    print(f"length of l_long: {len(l_long)}")
    print(f"length of l_short: {len(l_short)}")

    # for long sentences
    logging.info("for long sentences")
    arr_long_post = np.array([i["post_message"] for i in l_long])
    arr_long_id = np.array([i["live_sid"] for i in l_long])
    arr_short_post = np.array([i["post_message"] for i in l_short])
    arr_short_id = np.array([i["live_sid"] for i in l_short])

    print(f"length of arr_long_post: {len(arr_long_post)}")
    print(f"length of arr_long_id: {arr_long_id}")
    print(f"length of arr_short_post: {arr_short_post}")
    print(f"length of arr_short_id: {arr_short_id}")

    # AdRemover
    logging.info("AdRemover")
    adremover = AdRemover(arr_long_post)
    arr_long_1, arr_long_2 = adremover.fit
    arr_neu = adremover.transform(arr_long_1, arr_long_2)

    print(f"length of arr_neu: {len(arr_neu)}")

    # for short sentences
    logging.info("for short sentences")
    arr_post_neu = arr_long_post[arr_neu]
    arr_post_other = arr_long_post[~arr_neu]
    arr_id_neu = arr_long_id[arr_neu]
    arr_id_other = arr_long_id[~arr_neu]
    arr_long_pred_neu = np.array([0] * len(arr_post_neu))

    # for long sentences(run regex search)
    logging.info("long pred out")
    arr_long_pred_out = np.array(regex_sentiment(arr_post_other, l_regex))

    # for short sentences(run regex search)
    logging.info("short pred out")
    arr_short_pred_out = np.array(regex_sentiment(arr_short_post, l_regex))

    # prepare json output format
    logging.info("result json output")
    arr_result_post = np.concatenate((arr_post_neu, arr_post_other, arr_short_post))
    arr_result_ypred = np.concatenate((arr_long_pred_neu, arr_long_pred_out, arr_short_pred_out))
    arr_id = np.concatenate((arr_id_neu, arr_id_other, arr_short_id))

    l_result = [{"live_sid": str(i), "pred": int(j), "post_message": str(k)} for i, j, k in zip(arr_id, arr_result_ypred, arr_result_post)]
    print(f"length of l_result: {len(l_result)}")

    return Json({"results": l_result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True, port=os.getenv("POST"), debug=True)