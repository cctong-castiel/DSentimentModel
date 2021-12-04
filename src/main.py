# main.py

# mods
from os import getenv
import logging
from dotenv import load_dotenv
from sanic import Sanic
from sanic.response import json as Json, text
from scripts.model import sent_pipe
from scripts.func import get_config

# load env
load_dotenv()

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
    logging.info(f"length of p_data: {len(p_data)}")

    # prepare config
    # emoji_neg, emoji_pos, negative, neutral, positive
    logging.info("prepare config")
    l_regex = get_config()

    l_result = sent_pipe(l_regex, p_data)

    return Json({"results": l_result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=getenv("PORT"), debug=True)