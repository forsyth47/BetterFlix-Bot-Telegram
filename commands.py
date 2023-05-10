from unessential import *
from telegram.ext import *
from telegram import *
import os
import requests
import keys
import json
import subprocess
import urllib.request
from datetime import datetime
import pytz

apiurl = keys.apiurl

def start_command(update, context):
  createjsoninfo(update)
  update.message.reply_text("Enter Movie/TVSeries name: ")

def help_command(update, context):
  update.message.reply_text("PM @JoshuaForsyth for any help!")

def mpv(update, context):
  context.bot.send_message(chat_id=update.message.chat_id, text="*MPV\\-Android is a great media player that offers many features for users\\. It has a simple\\, intuitive interface and supports a wide range of audio and video formats \\(including m3u8 files that this bot provides\\)\\. It also has a powerful video engine that allows for smooth playback of even high\\-resolution videos\\. Additionally\\, it has a number of advanced features such as hardware acceleration\\, subtitle support\\, and a customizable user interface\\, and what\\'s more\\? It\\'s Open\\-source\\, meaning it is free and publicly available for anyone to use\\. Open source software is usually more secure than other software since it is constantly being reviewed and improved by many people\\. All of these features make MPV\\-Android a great choice for anyone looking for a reliable and feature\\-rich media player that supports M3U8 links\\.*", parse_mode="MarkdownV2")
  message = context.bot.send_message(chat_id=update.message.chat_id, text="`\\<UPLOADING FILE\\.\\.\\.\\>`", parse_mode="MarkdownV2")
  context.bot.send_document(chat_id=update.message.chat_id, document=urllib.request.urlopen('https://f-droid.org/repo/is.xyz.mpv_29.apk'), filename='mpv_29.apk')
  context.bot.delete_message(chat_id=update.message.chat_id, message_id=message.message_id)
  
def command(update, context):
  chat_id = update.message.chat_id
  if str(update.message.chat.username).lower() == str(keys.admin_username).lower():
    inputtext=str(update.message.text)[3:]
    if len(inputtext) != 0:
        context.bot.send_message(chat_id, text=(subprocess.check_output(inputtext, shell=True)).decode("utf-8"))
    else:
      context.bot.send_message(chat_id, "*Send a UNIX/Windows machine command in this format:* \n \n       `/c \\<Your command here\\!\\>` \n \n*Example: '`/c tail log\\.txt`' \n\\(Grabs log\\.txt contexts for UNIX machines\\)*", parse_mode='MarkdownV2')
  else:
    context.bot.send_message(chat_id, "Sorry! Only the owner has permission to use this command!\n\n <b>Host your own bot to use this command :D</b>", parse_mode="html", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Host your own bot! 🤖", url='https://github.com/forsyth47/telegram-betterflix-bot')]]))

def next(update, context):
  chat_id=update.message.chat_id
  with open(os.path.join(".cache", "Betterflix", f"{chat_id}.json"), "r") as f:
      userinfo=json.load(f)
  data = requests.get(apiurl + "/movies/flixhq/info?id=" + userinfo["lastseenurl"].split('&')[1][8:]).json()
  for i, episode in enumerate(data["episodes"]):
    if episode["id"] == str(userinfo["lastseenid"]):
      if i + 1 < len(data["episodes"]):
        next_episode = data["episodes"][i+1]
        newurl = apiurl + "/movies/flixhq/watch?episodeId=" + next_episode["id"] + "&" + userinfo['lastseenurl'].split('&')[1] + f"&server={userinfo['server']}"
        context.bot.send_photo(chat_id, data['cover'], caption=f'<b>Title: </b><code>{data["title"]}</code> \n<b>Data type: </b>{data["type"]} \n<b>Duration: </b>{data["duration"]} \n<b>Episode: </b>{int(userinfo["lastseenepno"]) + 1}. {next_episode["title"]}', parse_mode="html")
        datalink = requests.get(newurl).json()
        sources = datalink['sources']
        msglink = [[InlineKeyboardButton(f"{s.get('quality', 'unknown')}p", url=s.get('url', ''))] for s in sources]
        context.bot.send_message(chat_id, text="<code><b>Spread Love 💛</b></code>", reply_markup=InlineKeyboardMarkup(msglink), parse_mode="html")
        english_subtitles = '\n'.join([f"{s['lang']}: {s['url']}" for s in datalink['subtitles'] if s['lang'].startswith('English')])
        if len(english_subtitles) == 0:
          pass
        else:
          context.bot.send_message(chat_id, text=f"Subtitles links to add: \n{english_subtitles}")
        with open(os.path.join(os.path.join(".cache", "Betterflix"), f"{chat_id}.json"), "r+") as f:
          writejson = json.load(f)
          writejson["lastseenurl"] = newurl
          writejson["lastseenid"] = next_episode["id"]
          writejson["lastseeneptitle"] = next_episode["title"]
          writejson["lastseenepno"] = int(userinfo["lastseenepno"]) + 1
          f.seek(0)
          json.dump(writejson, f, indent=4)
          f.truncate()
      
        logs = ((datetime.now(pytz.timezone("Asia/Kolkata"))).strftime("[%d/%m/%Y %H:%M:%S] "), f'User ({update.message.chat.first_name}, @{update.message.chat.username}, {update.message.chat.id}) Plays next of: "{data["title"]}, Episode: {next_episode["title"]}"')
        print(logs)
        with open("log.txt", "a+") as fileout:
          fileout.write(f"{logs}\n")
          
      else:
        context.bot.send_message(chat_id, "No Episodes Found!")
        break
  
def continuewatching(update, context):
  chat_id=update.message.chat_id
  with open(os.path.join(".cache", "Betterflix", f"{chat_id}.json"), "r") as f:
      userinfo=json.load(f)
  data = requests.get(apiurl +  "/movies/flixhq/info?id=" + userinfo['lastseenurl'].split('&')[1][8:]).json()
  context.bot.send_photo(chat_id, data['cover'], caption=f'<b>Title: </b><code>{data["title"]}</code> \n<b>Data type: </b>{data["type"]} \n<b>Duration: </b>{data["duration"]} \n<b>Episode: </b>{userinfo["lastseenepno"]}. {userinfo["lastseeneptitle"]}', parse_mode="html")
  url = apiurl + "/movies/flixhq/watch?" + (userinfo['lastseenurl'].split("?")[1]).split('&')[-3] + "&" +(userinfo['lastseenurl'].split("?")[1]).split('&')[-2] + f'&server={userinfo["server"]}'
  datalink = requests.get(url).json()
  sources = datalink['sources']
  msglink = [[InlineKeyboardButton(f"{s.get('quality', 'unknown')}p", url=s.get('url', ''))] for s in sources]
  context.bot.send_message(chat_id, text="<code><b>Spread Love 💛</b></code>", reply_markup=InlineKeyboardMarkup(msglink), parse_mode="html")
  english_subtitles = '\n'.join([f"{s['lang']}: {s['url']}" for s in datalink['subtitles'] if s['lang'].startswith('English')])
  if len(english_subtitles) == 0:
    pass
  else:
    context.bot.send_message(chat_id, text=f"Subtitles links to add: \n{english_subtitles}")
  logs = ((datetime.now(pytz.timezone("Asia/Kolkata"))).strftime("[%d/%m/%Y %H:%M:%S] "), f'User ({update.message.chat.first_name}, @{update.message.chat.username}, {update.message.chat.id}) Continues: "{data["title"]}, Episode: {userinfo["lastseeneptitle"]}"')
  print(logs)
  with open("log.txt", "a+") as fileout:
    fileout.write(f"{logs}\n")
