import requests
import json
import os
from datetime import datetime
from telegram import *
from telegram.ext import *
from webserver import keep_alive
import keys
import pytz
import subprocess
import inspect
import re

keep_alive()
print("Starting...")

#apiurl = "https://api.consumet.org"
#apiurl = "https://api.animxeast.eu.org"
#apiurl = "https://entertainment-scrapper.vercel.app"
#
#apiurl = "https://c.delusionz.xyz"
#apiurl = "https://apiconsumetorg-1.forsyth47.repl.co"
apiurl = "https://api.haikei.xyz"


def start_command(update, context):
  #update.message.reply_text("Use pickamovieforme.com to pick a movie according to you mood! ")
  update.message.reply_text("Enter Movie/TVSeries name: ")

def help_command(update, context):
  update.message.reply_text("⚠️ If the bot doesn't reply after selecting source, try another source! ⚠️")
  update.message.reply_text("PM @JoshuaForsyth for any help!")

def watch2gether(update, context):
  context.bot.send_message(update.message.chat_id, """Use app.watchpubs.com """)

def how2play(update, context):
  global ufid
  ufid = inspect.stack()[0][3]
  linuxbutton = InlineKeyboardButton('Linux', callback_data="1")
  windowsbutton = InlineKeyboardButton('Windows', callback_data="2")
  androidbutton = InlineKeyboardButton('Android', callback_data="3")
  browserbutton = InlineKeyboardButton('Browser', callback_data="4")
  replymarkup = InlineKeyboardMarkup([[linuxbutton, windowsbutton],[androidbutton, browserbutton]])
  context.bot.send_message(update.message.chat_id, "Select your device: ", ReplyMarkup=replymarkup)
  
def mpv(update, context):
  chat_id=update.message.chat_id

  context.bot.send_message(chat_id, text="MPV-Android is a great media player that offers many features for users. It has a simple, intuitive interface and supports a wide range of audio and video formats (including m3u8 files that this bot provides). It also has a powerful video engine that allows for smooth playback of even high-resolution videos. Additionally, it has a number of advanced features such as hardware acceleration, subtitle support, and a customizable user interface, and what's more? It's Open-source, meaning it is free and publicly available for anyone to use. Open source software is usually more secure than other software since it is constantly being reviewed and improved by many people. All of these features make MPV-Android a great choice for anyone looking for a reliable and feature-rich media player.")
  context.bot.send_message(chat_id, text="You can either download it from playstore or from official mpv fdroid repository from the link given below 👇")
  context.bot.send_message(chat_id, text="https://f-droid.org/repo/is.xyz.mpv_29.apk 💚")
  
def com(update, context):
  comtext = str(update.message.text).lower()
  comtext = comtext[4:]
  comout = subprocess.check_output(comtext, shell=True)
  comout = comout.decode("utf-8")
  chat_id = update.message.chat_id
  context.bot.send_message(chat_id, comout)

is_restarting = False

def defsearch(update, context):
  global is_restarting
  global ufid
  ufid = inspect.stack()[0][3]
  global chat_id
  global search_input
  global resultsearch
  #-----------log------------
  message_type = update.message.chat.type
  textrq = str(update.message.text).lower()
  logtext = textrq  #[7:]

  nowx = datetime.now(pytz.timezone("Asia/Kolkata"))
  # Print a log for debugging
  logsss = (
    nowx.strftime("[%d/%m/%Y %H:%M:%S] "),
    f'User ({update.message.chat.first_name}, {update.message.chat.username}, {update.message.chat.id}) says: "{logtext}" in: {message_type}'
  )
  print(logsss)
  fileout = open("log.txt", "a+")
  fileout.writelines(logsss)
  fileout.writelines("\n")
  fileout.close()
  #-----------log------------

  
  chat_id = update.message.chat_id
  moviename = str(update.message.text).lower()
  #moviename = moviename[5:]
  moviename = str(moviename)
  urlsearch = apiurl + "/movies/flixhq/" + moviename
  responsesearch = requests.get(urlsearch, params={"page": 1})
  datasearch = responsesearch.json()
  jsonsearch = json.dumps(datasearch, indent=4)
  #print (jsonsearch)
  resultsearch = datasearch['results']
  keyboard = []
  for i, resultidkvar in enumerate(resultsearch):
    button = InlineKeyboardButton(f"{i + 1}. {resultidkvar['title']}",
                                  callback_data=f"{i + 1}")
    keyboard.append([button])

  exit_button = InlineKeyboardButton("Exit", callback_data="exit")
  keyboard.append([exit_button])
  reply_markup = InlineKeyboardMarkup(keyboard)
  context.bot.send_message(chat_id,
                           text="Select the desired title:",
                           reply_markup=reply_markup)


def defid(update, context) -> str:
  global ufid
  ufid = inspect.stack()[0][3]
  global movieid
  global datamovie
  global chat_id
  movieid = movieid
  if movieid.startswith("tv/"):
    movieidstripped = movieid[3:]
    urlmovie = apiurl + "/movies/flixhq/info?id=tv/" + movieidstripped
  else:
    movieidstripped = movieid[6:]
    urlmovie = apiurl + "/movies/flixhq/info?id=movie/" + movieidstripped
  responsemovie = requests.get(urlmovie)
  print ("here is: " + str(responsemovie))
  datamovie = responsemovie.json()
  jsonmovie = json.dumps(datamovie, indent=4)
  #print (datamovie["image"])
  context.bot.send_photo(
    chat_id, datamovie["cover"],
    caption="Plot summary: " + datamovie["description"] + "\n" + "\n" + "Data type: " +
    datamovie["type"] + "\n" + "Released on: " + datamovie["releaseDate"])
  keyboard = []
  for i, idvaridk in enumerate(datamovie['episodes']):
    button = InlineKeyboardButton(f"{i + 1}. {idvaridk['title']}",
                                  callback_data=f"{i + 1}")
    keyboard.append([button])

  exit_button = InlineKeyboardButton("Exit", callback_data="exit")
  keyboard.append([exit_button])
  reply_markup = InlineKeyboardMarkup(keyboard)
  context.bot.send_message(chat_id,
                           text="Select the desired episode: ",
                           reply_markup=reply_markup)


def defep(update, context):
  global ufid
  ufid = inspect.stack()[0][3]
  global datamovieid
  global dataep
  global movieid
  global chat_id
  urlep = apiurl + "/movies/flixhq/servers"
  responseep = requests.get(urlep,
                            params={
                              "episodeId": datamovieid,
                              "mediaId": movieid
                            })
  dataep = responseep.json()
  jsonep = json.dumps(dataep, indent=4)
  keyboard = []
  for i, episode in enumerate(dataep):
    #print(f"{i+1}: {episode['name']}")
    button = InlineKeyboardButton(f"{i + 1}. {episode['name']}",
                                  callback_data=f"{i + 1}")
    keyboard.append([button])

  exit_button = InlineKeyboardButton("Exit", callback_data="exit")
  keyboard.append([exit_button])
  reply_markup = InlineKeyboardMarkup(keyboard)
  context.bot.send_message(chat_id, text="Select the desired Server: ", reply_markup=reply_markup)
  print()
  #link_input = int(input("Enter a Server (1/2/3/...): "))
  #selected_url = dataep[link_input - 1]["name"]


def deflink(update, context):
  global datamovieid
  global movieid
  global selected_url
  global chat_id
  global datalink
  urllink = apiurl + "/movies/flixhq/watch"
  responselink = requests.get(urllink, params={"episodeId": datamovieid, "mediaId": movieid, "server": selected_url})
  print (responselink)
  datalink = responselink.json()
  jsonlink = json.dumps(datalink, indent=4)
  sources = datalink['sources']
  print("----------------")
  print (responselink)
  print("----------------")
  msglink = ""
  for i, sourceidkvar in enumerate(sources):
    msg = f"Quality: {sourceidkvar['quality']}" + "\n" + f"isM3U8: {sourceidkvar['isM3U8']}" + "\n" + f"URL:    {sourceidkvar['url']}" + "\n"
    msglink += msg
    msglink += "\n"
    msglink += "\n"
  
  english_subtitles = ""
  for subtitle in datalink["subtitles"]:
    if subtitle["lang"].startswith("English"):
      english_subtitles += subtitle["lang"] + ": " + subtitle["url"] + "\n"
      english_subtitles += "\n"
      #english_subtitles.append(english_subtitle)  
  #english_subtitles_json = json.dumps(english_subtitles)
  linkandsubs = msglink + "\n" + "Subtitles links to add: " + "\n" + english_subtitles
  
  #context.bot.send_message(chat_id, text=msglink)
  context.bot.send_message(chat_id, text=linkandsubs)
    #print("\n")
    #print(f"Quality: {sourceidkvar['quality']}")
    #print(f"isM3u8: {sourceidkvar['isM3U8']}")
    #print(f"url: {sourceidkvar['url']}")
    #print("\n")

def button1(update, context):
  global resultsearch
  global movieid
  global datamovie
  global datamovieid
  global dataep
  global datalink
  global selected_url
  global chat_id
  global ufid
  query = update.callback_query
  data = query.data
  if data == "exit":
    context.bot.answerCallbackQuery(callback_query_id=query.id, text="Exited")
    context.bot.answerCallbackQuery(callback_query_id=query.id, text="Enter a Movie/TVShow name.")
    update.callback_query.edit_message_reply_markup(None)
    return
  search_input = int(data)
  context.bot.answerCallbackQuery(callback_query_id=query.id, text="Selected")
  update.callback_query.edit_message_reply_markup(None)
  if ufid == "defsearch":
    movieid = resultsearch[search_input - 1]['id']
    defid(update, context)
  elif ufid == "defid":
    datamovieid = datamovie['episodes'][search_input - 1]['id']
    defep(update, context)
  elif ufid == "defep":
    selected_url = dataep[search_input - 1]["name"]
    deflink(update, context)
  elif ufid == "how2play":
    if data == 1:
      context.bot.send_message(update.message.chat_id, "For linux: ")
    
  else:
    context.bot.send_message(chat_id, text="Error! Make new request")
    


def handle_message(update, context):
  # Get basic info of the incoming message
  message_type = update.message.chat.type
  
  logtext = text  #[7:]

  nowx = datetime.now(pytz.timezone("Asia/Kolkata"))
  # Print a log for debugging
  logsss = (
    nowx.strftime("[%d/%m/%Y %H:%M:%S] "),
    f'User ({update.message.chat.username}, {update.message.chat.id}) says: "{text}" in: {message_type}'
  )
  print(logsss)

  # React to group messages only if users mention the bot directly
  if message_type == 'group':
    # Replace with your bot username
    if '@flixhqbot' in text:
      new_text = text.replace('@flixhqbot', '').strip()
      response =defsearch(new_text)
  else:
    response = defsearch(text)

  # Reply normal if the message is in private
  update.message.reply_text(response)

  #print log in file.
  fileout = open("log.txt", "a+")
  fileout.writelines(logsss)
  fileout.writelines("\n")
  fileout.close()


# Log errors
def error(update, context):
  nowx = datetime.now(pytz.timezone("Asia/Kolkata"))
  global errorout
  errorout = (nowx.strftime("[%d/%m/%Y %H:%M:%S] "),
              f'Update {update} caused error {context.error}')
  print(errorout)


# Run the program #use_context=True,
if __name__ == '__main__':
  updater = Updater(keys.token, use_context=True)
  dp = updater.dispatcher

  # Commands
  dp.add_handler(CommandHandler('start', start_command))
  dp.add_handler(CommandHandler('help', help_command))
  dp.add_handler(CommandHandler('com', com))
  dp.add_handler(CommandHandler('mxplayer', mpv))
  dp.add_handler(CommandHandler('androidplayer', mpv))
  dp.add_handler(CommandHandler('watch2gether', watch2gether))
  #dp.add_handler(CommandHandler('restart', restart_handler))
  
  #dp.add_handler(CommandHandler('name', name))
  dp.add_handler(MessageHandler(Filters.text, defsearch))
  #dp.add_handler(CommandHandler('defid', defid))
  #dp.add_handler(ConversationHandler(LOCATION: MessageHandler(Filters.text, name)))
  # add button handler to dispatcher
  dp.add_handler(CallbackQueryHandler(button1))

  # Messages

  dp.add_handler(MessageHandler(Filters.text, handle_message))

  # Log all errors
  dp.add_error_handler(error)

  # Run the bot
  updater.start_polling(1.0)
  updater.idle()
