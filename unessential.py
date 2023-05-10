import os
import subprocess
import json
import keys
from telegram import *
from telegram.ext import *

apiurl = keys.apiurl

def createjsoninfo(update):
  cache_dir = os.path.join(".cache", "Betterflix")
  if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
  data_file = os.path.join(cache_dir, f"{update.message.chat_id}.json")
  if not os.path.exists(data_file) or len(str((subprocess.check_output("cat "+data_file, shell=True)).decode("utf-8")))==0:
    with open(data_file, "w") as f:
      json.dump({"FirstName":update.message.chat.first_name, "chat_id":update.message.chat_id, "lastseenurl": f"{apiurl}/movies/flixhq/watch?episodeId=255412&mediaId=tv/watch-tom-and-jerry-tales-37606&server=upcloud", "server":"upcloud", "lastseenid": "255412", "lastseeneptitle": "Eps 1: Tiger Cat / Feeding Time / Polar Peril", "lastseenepno": 1}, f, indent=4)

def cachecre():
	if not os.path.exists('cache'):
		os.mkdir('cache')