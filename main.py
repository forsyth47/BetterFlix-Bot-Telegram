import os
import inspect
import json
import subprocess
import urllib.request
from datetime import datetime
import time
import keys
import pytz
import requests
from webserver import keep_alive
from telegram import *
from telegram.ext import *
from gitnotifier import *
from unessential import *
from commands import *

apiurl = keys.apiurl
keep_alive()

#==================================COMMANDS==================================


def changeserver(update, context):
  global ufid
  global chat_id
  global messagechangeserver
  ufid = inspect.stack()[0][3]
  chat_id=update.message.chat_id
  with open(os.path.join(".cache", "Betterflix", f"{chat_id}.json"), "r") as f:
      userinfo=json.load(f)
  keyboard = [[InlineKeyboardButton("Default", callback_data='1')], [InlineKeyboardButton("UPCLOUD", callback_data='2')], [InlineKeyboardButton("VIDCLOUD", callback_data='3')]]
  messagechangeserver=context.bot.send_message(chat_id, text=f"Current selection: <code>{userinfo['server']}</code> \nSelect the Server :", parse_mode="html", reply_markup=InlineKeyboardMarkup(keyboard))

#==================================COMMANDS-END==================================



#==================================SEARCH-MOVIE-SHOW==================================

def search(update, context):
  global ufid
  global chat_id
  global messagesearch
  global resultsearch
  global requestsearch
  global userinfo
  logs = ((datetime.now(pytz.timezone("Asia/Kolkata"))).strftime("[%d/%m/%Y %H:%M:%S] "), f'User ({update.message.chat.first_name}, @{update.message.chat.username}, {update.message.chat.id}) says: "{str(update.message.text).lower()}"')
  print(logs)
  with open("log.txt", "a+") as fileout:
    fileout.write(f"{logs}\n")
  createjsoninfo(update)
  ufid = inspect.stack()[0][3]
  chat_id = update.message.chat_id
  requestsearch=update.message
  with open(os.path.join(".cache", "Betterflix", f"{chat_id}.json"), "r") as f:
      userinfo=json.load(f)
  urlsearch = apiurl + "/movies/flixhq/" + str(update.message.text).lower()
  responsesearch = requests.get(urlsearch, params={"page": 1})
  datasearch = responsesearch.json()
  resultsearch = datasearch['results']
  keyboard = [[InlineKeyboardButton(f"{i + 1}. {tempsearch['title']}", callback_data=f"{i + 1}")]for i, tempsearch in enumerate(resultsearch)] + [[InlineKeyboardButton("> EXIT", callback_data="exit")]]
  messagesearch = context.bot.send_message(chat_id, text="Select the desired title:", reply_markup=InlineKeyboardMarkup(keyboard))


#==================================SEARCH-MOVIE-SHOW-END==================================


#==================================Choosing-EPisode==================================

def cep(update, context):
  global ufid
  global datacep
  global messagecep
  global dataid
  ufid = inspect.stack()[0][3]
  if idsearch.startswith("tv/"):
    responsecep = requests.get(apiurl + "/movies/flixhq/info?id=tv/" + idsearch[3:])
  else:
    responsecep = requests.get(apiurl + "/movies/flixhq/info?id=movie/" + idsearch[6:])
  dataid = datacep = responsecep.json()
  #print(json.dumps(dataid, indent=4))
  context.bot.send_photo(chat_id, dataid["cover"], caption=f'<b>Title: </b><code>{dataid["title"]}</code> \n<b>Plot summary: </b>{dataid["description"][9:]} \n<b>Total Episodes: </b> {len(datacep["episodes"])} \n<b>Data type: </b>{dataid["type"]} \n<b>Released on: </b>{dataid["releaseDate"]} \n<b>Production: </b><code>{dataid["production"]}</code> \n<b>Duration: </b>{dataid["duration"]} \n<b>IMDb Rating: </b>{dataid["rating"]}', parse_mode="html")

  send_pagination(update, context, 1)

def send_pagination(update, context, page):
  global udid
  global messagecep
  ufid = inspect.stack()[0][3]
  keyboard = []
  STEP = 97
  start_index = (page - 1) * STEP
  end_index = min(start_index + STEP, len(datacep['episodes']))
  for i in range(start_index, end_index):
    tempcep = datacep['episodes'][i]
    keyboard.append([InlineKeyboardButton(f"{i+1}. {tempcep['title']}", callback_data=f"{i + 1}")])
  if page > 1:
    keyboard.append([InlineKeyboardButton("◀️ PREVIOUS", callback_data="888")])
  if end_index < len(datacep['episodes']):
    keyboard.append([InlineKeyboardButton("NEXT ▶️", callback_data="999")])
  keyboard.append([InlineKeyboardButton(f"> EXIT <", callback_data="exit")])
  messagecep = context.bot.send_message(chat_id, text=f"Select the desired Episode\n<b>Current Page: </b>{page}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="html")

#==================================Choosing-EPisode-END==================================


#==================================grabbin-the-LINK(s)==================================

def link(update, context):
  data = requests.get(apiurl + "/movies/flixhq/watch", params={"episodeId": idcep, "mediaId": idsearch, "server": userinfo["server"]}).json()
  #print(json.dumps(data, indent=4))
  sources = data['sources']
  msglink = [[InlineKeyboardButton(f"{s.get('quality', 'unknown')}p", url=s.get('url', ''))] for s in sources]
  quotejson=requests.get('https://api.quotable.io/random').json()
  context.bot.send_message(chat_id, text=f"<b>{quotejson['content']}</b>\n~<code>{quotejson['author']}</code>", reply_markup=InlineKeyboardMarkup(msglink), parse_mode="html")
  english_subtitles = '\n'.join([f"{s['lang']}: {s['url']}" for s in data['subtitles'] if s['lang'].startswith('English')])
  if len(english_subtitles) == 0:
    pass
  else:
    context.bot.send_message(chat_id, text=f"Subtitles links to add: \n{english_subtitles}")

  with open(os.path.join(os.path.join(".cache", "Betterflix"), f"{chat_id}.json"), "r+") as f:
    writejson = json.load(f)
    writejson["lastseenurl"] = apiurl + f"/movies/flixhq/watch?episodeId={idcep}&mediaId={idsearch}&server={userinfo['server']}"
    writejson["lastseenid"] = idcep
    writejson["lastseeneptitle"] = eptitlecep
    f.seek(0)
    json.dump(writejson, f, indent=4)
    f.truncate()


#==================================SEARCH-MOVIE-SHOW-END==================================



# Log errors
def error(update, context):
  print ((datetime.now(pytz.timezone("Asia/Kolkata"))).strftime("[%d/%m/%Y %H:%M:%S] "), f'Update {update} caused error {context.error}')

#==================================CALLBACKQUERYBUTTON==================================

def Button(update, context):
  global resultsearch
  global idsearch
  global idcep
  global eptitlecep
  global idcserver
  query = update.callback_query
  data = query.data
  if data == "exit":
    context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Exited")
    update.callback_query.edit_message_reply_markup(None)
    if ufid == "search":
      context.bot.delete_message(chat_id, message_id=messagesearch.message_id)
    elif ufid == "cep":
      context.bot.delete_message(chat_id, message_id=messagecep.message_id)
    return ("Make Another Search: ")
  buttoncallback = int(data)
  context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Selected")
  update.callback_query.edit_message_reply_markup(None)
  if ufid == "search":
    idsearch = resultsearch[buttoncallback - 1]['id']
    context.bot.delete_message(chat_id, message_id=messagesearch.message_id)
    cep(update, context)
  elif ufid == "cep":
    if buttoncallback == 888:
        page = int(query.message.text.split()[-1]) - 1
        query.answer()
        context.bot.delete_message(chat_id, message_id=messagecep.message_id)
        send_pagination(update, context, page)
    elif buttoncallback == 999:
        page = int(query.message.text.split()[-1]) + 1
        query.answer()
        context.bot.delete_message(chat_id, message_id=messagecep.message_id)
        send_pagination(update, context, page)
    else:
      idcep = datacep['episodes'][buttoncallback - 1]['id']
      eptitlecep = datacep['episodes'][buttoncallback - 1]['title']
      with open(os.path.join(os.path.join(".cache", "Betterflix"), f"{chat_id}.json"), "r+") as f:
          writejson = json.load(f)
          writejson["lastseenepno"] = buttoncallback
          f.seek(0)
          json.dump(writejson, f, indent=4)
          f.truncate()
      context.bot.delete_message(chat_id, message_id=messagecep.message_id)
      link(update, context)
  elif ufid=="changeserver":
      if buttoncallback==1:
        with open(os.path.join(os.path.join(".cache", "Betterflix"), f"{chat_id}.json"), "r+") as f:
          writejson = json.load(f)
          writejson["server"] = "upcloud"
          f.seek(0)
          json.dump(writejson, f, indent=4)
          f.truncate()
      elif buttoncallback==2:
        with open(os.path.join(os.path.join(".cache", "Betterflix"), f"{chat_id}.json"), "r+") as f:
          writejson = json.load(f)
          writejson["server"] = "vidcloud"
          f.seek(0)
          json.dump(writejson, f, indent=4)
          f.truncate()
      context.bot.delete_message(chat_id, message_id=messagechangeserver.message_id)
      context.bot.send_message(chat_id, "Preference have been saved!")
  elif ufid == "howtouse":
    if data == 1:
      context.bot.send_message(update.message.chat_id, "For linux: ")
    
  else:
    context.bot.send_message(chat_id, text="Error! Make new request")
    
#==================================CALLBACKQUERYBUTTON-END==================================


#================================== STARTING THE PROGRAM ==================================
if __name__ == '__main__':
  print("===================Starting BetterFlix-Bot-Telegram===================")
  updater = Updater(keys.token, use_context=True)
  dp = updater.dispatcher

  # Commands
  #dp.add_handler(CommandHandler('name', name))
  dp.add_handler(CommandHandler('start', start_command))
  dp.add_handler(CommandHandler('help', help_command))
  dp.add_handler(CommandHandler('c', command))
  dp.add_handler(CommandHandler('mpv', mpv))
  dp.add_handler(CommandHandler('source', changeserver))
  dp.add_handler(CommandHandler('next', next))
  dp.add_handler(CommandHandler('continue', continuewatching))

  # Messages
  dp.add_handler(MessageHandler(Filters.text, search))
  
  # InlineKeyboardButton
  dp.add_handler(CallbackQueryHandler(Button))

  # Log all errors
  dp.add_error_handler(error)

  # Run the bot
  updater.start_polling(1.0)

  while True:
    check_for_commits()
    time.sleep(600) # Sleep for an hour before checking again

  updater.idle()

#================================== END OF THW SCRIPT ==================================