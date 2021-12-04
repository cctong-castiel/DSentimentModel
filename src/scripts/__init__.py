import json
from os import getcwd
from os.path import join

# threashold score
tunnings = json.load(open(join(getcwd(), "config/tunning.json"), "r"))