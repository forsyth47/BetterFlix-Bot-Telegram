#pip install python-telegram-bot==13.15 flask python-dotenv
#==================================IMPORTS & API==================================
import inspect
import json
import subprocess
import urllib.request
from datetime import datetime
import requests
import pytz
from webserver import keep_alive
import keys
from telegram import *
from telegram.ext import *

#apiurl = "https://api.consumet.org"
#apiurl = "https://api.animxeast.eu.org"
#apiurl = "https://c.delusionz.xyz"
apiurl = "https://api.haikei.xyz"
#==================================IMPORTS & API END==================================

def howtouse(update, context):
  global ufid
  ufid = inspect.stack()[0][3]
  linuxbutton = InlineKeyboardButton('Linux', callback_data="1")
  windowsbutton = InlineKeyboardButton('Windows', callback_data="2")
  androidbutton = InlineKeyboardButton('Android', callback_data="3")
  browserbutton = InlineKeyboardButton('Browser', callback_data="4")
  replymarkup = InlineKeyboardMarkup([[linuxbutton, windowsbutton],[androidbutton, browserbutton]])
  context.bot.send_message(update.message.chat_id, "Select your device: ", ReplyMarkup=replymarkup)
  

#==================================COMMANDS==================================

def start_command(update, context):
  update.message.reply_text("Enter Movie/TVSeries name: ")

def help_command(update, context):
  update.message.reply_text("PM @JoshuaForsyth for any help!")

def mpv(update, context):
  context.bot.send_message(chat_id=update.message.chat_id, text="*MPV\\-Android is a great media player that offers many features for users\\. It has a simple\\, intuitive interface and supports a wide range of audio and video formats \\(including m3u8 files that this bot provides\\)\\. It also has a powerful video engine that allows for smooth playback of even high\\-resolution videos\\. Additionally\\, it has a number of advanced features such as hardware acceleration\\, subtitle support\\, and a customizable user interface\\, and what\\'s more\\? It\\'s Open\\-source\\, meaning it is free and publicly available for anyone to use\\. Open source software is usually more secure than other software since it is constantly being reviewed and improved by many people\\. All of these features make MPV\\-Android a great choice for anyone looking for a reliable and feature\\-rich media player that supports M3U8 links\\.*", parse_mode="MarkdownV2")
  message = context.bot.send_message(chat_id=update.message.chat_id, text="`\\<UPLOADING FILE\\.\\.\\.\\>`", parse_mode="MarkdownV2")
  context.bot.send_document(chat_id=update.message.chat_id, document=urllib.request.urlopen('https://f-droid.org/repo/is.xyz.mpv_29.apk'), filename='mpv_29.apk')
  context.bot.delete_message(chat_id=update.message.chat_id, message_id=upsendmessage.message_id)
  
def command(update, context):
  chat_id = update.message.chat_id
  if str(update.message.chat.username).lower() == str(keys.admin_username).lower():
    inputtext=str(update.message.text)[8:]
    if len(inputtext) != 0:
        context.bot.send_message(chat_id, text=(subprocess.check_output(inputtext, shell=True)).decode("utf-8"))
    else:
      context.bot.send_message(chat_id, "*Send a UNIX/Windows machine command in this format:* \n \n       `/command \\<Your command here\\!\\>` \n \n*Example: '`/command tail log\\.txt`' \n\\(Grabs log\\.txt contexts for UNIX machines\\)*", parse_mode='MarkdownV2')
  else:
    context.bot.send_message(chat_id, "You do not have the permission to use this command!")

#==================================COMMANDS-END==================================


#==================================SEARCH-MOVIE-SHOW==================================

def search(update, context):
  global ufid
  global chat_id
  global messagesearch
  global resultsearch
  global requestsearch

  ##===================logging===================
  logs = ((datetime.now(pytz.timezone("Asia/Kolkata"))).strftime("[%d/%m/%Y %H:%M:%S] "), f'User ({update.message.chat.first_name}, @{update.message.chat.username}, {update.message.chat.id}) says: "{str(update.message.text).lower()}" in: {update.message.chat.type}')
  print(logs)
  with open("log.txt", "a+") as fileout:
    fileout.write(f"{logs}\n")
  ##===================logging-end===================
  ufid = inspect.stack()[0][3]
  chat_id = update.message.chat_id
  requestsearch=update.message
  urlsearch = apiurl + "/movies/flixhq/" + str(update.message.text).lower()
  responsesearch = requests.get(urlsearch, params={"page": 1})
  datasearch = responsesearch.json()
  #print(json.dumps(datasearch, indent=4))
  resultsearch = datasearch['results']
  ##===================Making-InlineKeyboardButton-with-Search-Results===================
  keyboard = []
  for i, tempsearch in enumerate(resultsearch):
    keyboard.append([InlineKeyboardButton(f"{i + 1}. {tempsearch['title']}", callback_data=f"{i + 1}")])
  keyboard.append([InlineKeyboardButton(">>> EXIT <<<", callback_data="exit")])
  messagesearch = context.bot.send_message(chat_id, text="Select the desired title:", reply_markup=InlineKeyboardMarkup(keyboard))

  ##===================Making-InlineKeyboardButton-with-Search-Results-End===================

#==================================SEARCH-MOVIE-SHOW-END==================================


#==================================Choosing-EPisode==================================

def cep(update, context):
  global ufid
  global datacep
  global messagecep
  ufid = inspect.stack()[0][3]
  if idsearch.startswith("tv/"):
    responsecep = requests.get(apiurl + "/movies/flixhq/info?id=tv/" + idsearch[3:])
  else:
    responsecep = requests.get(apiurl + "/movies/flixhq/info?id=movie/" + idsearch[6:])
  dataid = datacep = responsecep.json()
  #print(json.dumps(dataid, indent=4))
  #context.bot.send_photo(chat_id, dataid["cover"], caption=f'<b><i>Title: </i></b><code>{dataid["title"]}</code> \n<b><i>Plot summary: </i></b>{dataid["description"][9:]} \n<b><i>Data type: </i></b>{dataid["type"]} \n<b><i>Released on: </i></b>{dataid["releaseDate"]} \n<b><i>Production: </i></b><code>{dataid["production"]}</code> \n<b><i>Duration: </i></b>{dataid["duration"]} \n<b><i>IMDb Rating: </i></b>{dataid["rating"]}', parse_mode="html")
  context.bot.send_photo(chat_id, dataid["cover"], caption=f'<b>Title: </b><code>{dataid["title"]}</code> \n<b>Plot summary: </b>{dataid["description"][9:]} \n<b>Data type: </b>{dataid["type"]} \n<b>Released on: </b>{dataid["releaseDate"]} \n<b>Production: </b><code>{dataid["production"]}</code> \n<b>Duration: </b>{dataid["duration"]} \n<b>IMDb Rating: </b>{dataid["rating"]}', parse_mode="html")
  #context.bot.send_photo(chat_id, dataid["cover"], caption=f'<b>Title: </b><code>{dataid["title"]}</code> \n<b>Plot summary: </b><code>{dataid["description"][9:]}</code> \n<b>Data type: </b><code>{dataid["type"]}</code> \n<b>Released on: </b><code>{dataid["releaseDate"]}</code> \n<b>Production: </b><code>{dataid["production"]}</code> \n<b>Duration: </b><code>{dataid["duration"]}</code> \n<b>IMDb Rating: </b><code>{dataid["rating"]}</code>', parse_mode="html")
  keyboard = []
  for i, tempcep in enumerate(datacep['episodes']):
    keyboard.append([InlineKeyboardButton(f"{i + 1}. {tempcep['title']}", callback_data=f"{i + 1}")])
  keyboard.append([InlineKeyboardButton(">>> EXIT <<<", callback_data="exit")])
  messagecep = context.bot.send_message(chat_id, text="Select the desired episode: ", reply_markup=InlineKeyboardMarkup(keyboard))

#==================================Choosing-EPisode-END==================================


#==================================Choosing-SERVER==================================

def cserver(update, context):
  global ufid
  global datacserver
  global messagecserver
  ufid = inspect.stack()[0][3]
  datacserver = (requests.get(apiurl + "/movies/flixhq/servers", params={"episodeId": idcep, "mediaId": idsearch})).json()
  keyboard = [[InlineKeyboardButton(f"{i + 1}. {tempcserver['name']}", callback_data=f"{i + 1}")]for i, tempcserver in enumerate(datacserver)] + [[InlineKeyboardButton(">>> EXIT <<<", callback_data="exit")]]
  messagecserver=context.bot.send_message(chat_id, text="Select the desired Server: ", reply_markup=InlineKeyboardMarkup(keyboard))

#==================================Choosing-SERVER==================================


#==================================grabbin-the-LINK(s)==================================

def link(update, context):
  data = requests.get(apiurl + "/movies/flixhq/watch", params={"episodeId": idcep, "mediaId": idsearch, "server": idcserver}).json()
  sources = data['sources']
  msglink = [[InlineKeyboardButton(f"{s.get('quality', 'unknown')}p", url=s.get('url', ''))] for s in sources]
  context.bot.send_message(chat_id, text=f"<b>{(requests.get('https://api.quotable.io/random').json())['content']}</b>\n~<code>{(requests.get('https://api.quotable.io/random').json())['author']}</code>", reply_markup=InlineKeyboardMarkup(msglink), parse_mode="html")
  english_subtitles = '\n'.join([f"{s['lang']}: {s['url']}" for s in data['subtitles'] if s['lang'].startswith('English') or s['lang'].startswith('Default')])
  context.bot.send_message(chat_id, text=f"Subtitles links to add: \n{english_subtitles}")

#==================================SEARCH-MOVIE-SHOW-END==================================

#==================================CALLBACKQUERYBUTTON==================================

def Button(update, context):
  global resultsearch
  global idsearch
  global idcep
  global idcserver
  data = update.callback_query.data
  if data == "exit":
    context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Exited")
    update.callback_query.edit_message_reply_markup(None)
    return
  buttoncallback = int(data)
  context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Selected")
  update.callback_query.edit_message_reply_markup(None)
  if ufid == "search":
    idsearch = resultsearch[buttoncallback - 1]['id']
    context.bot.delete_message(chat_id, message_id=messagesearch.message_id)
    cep(update, context)
  elif ufid == "cep":
    idcep = datacep['episodes'][buttoncallback - 1]['id']
    context.bot.delete_message(chat_id, message_id=messagecep.message_id)
    cserver(update, context)
  elif ufid == "cserver":
    idcserver = datacserver[buttoncallback - 1]["name"]
    context.bot.delete_message(chat_id, message_id=messagecserver.message_id)
    link(update, context)
  elif ufid == "howtouse":
    if data == 1:
      context.bot.send_message(update.message.chat_id, "For linux: ")
    
  else:
    context.bot.send_message(chat_id, text="Error! Make new request")
    
#==================================CALLBACKQUERYBUTTON-END==================================

#================================== OTHER GENERAL STUFF ==================================

# Log errors
def error(update, context):
  print ((datetime.now(pytz.timezone("Asia/Kolkata"))).strftime("[%d/%m/%Y %H:%M:%S] "), f'Update {update} caused error {context.error}')


#================================== OTHER GENERAL STUFF END ==================================

#================================== STARTING THE PROGRAM ==================================
if __name__ == '__main__':
  keep_alive()
  print("===================Starting Telegram-Betterflix-Bot===================")
  updater = Updater(keys.token, use_context=True)
  dp = updater.dispatcher

  # Commands
  #dp.add_handler(CommandHandler('name', name))
  dp.add_handler(CommandHandler('start', start_command))
  dp.add_handler(CommandHandler('help', help_command))
  dp.add_handler(CommandHandler('command', command))
  dp.add_handler(CommandHandler('mpv', mpv))

  # Messages
  dp.add_handler(MessageHandler(Filters.text, search))
  
  # InlineKeyboardButton
  dp.add_handler(CallbackQueryHandler(Button))

  # Log all errors
  dp.add_error_handler(error)

  # Run the bot
  updater.start_polling(1.0)
  updater.idle()

#================================== END OF THW SCRIPT ==================================