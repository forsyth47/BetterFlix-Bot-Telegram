import requests
import json
import os
import telegram
import subprocess

def check_for_commits():
    # Set the API endpoint URL and repository information
	url = 'https://api.github.com/repos/forsyth47/BetterFlix-Bot-Telegram/commits'
    
    # Set the headers to include your GitHub username and personal access token
	headers = {'Authorization': os.environ['send-commit-msg-token']}
    
    # Get the latest commit information
	response = requests.get(url, headers=headers)
	response_json = response.json()
	latest_commit = response_json[0]
	
    
	if not os.path.exists('data'):
		os.mkdir('data')
	if not os.path.exists('data/commit_info.json') or len(str((subprocess.check_output("cat "+'data/commit_info.json', shell=True)).decode("utf-8")))==0:
		with open('data/commit_info.json', 'w') as f:
			json.dump(latest_commit, f, indent=4)
	with open('data/commit_info.json', 'r') as f:
			last_commit = json.load(f)
        
    

	if last_commit['sha'] != latest_commit['sha']:
		with open('data/commit_info.json', 'w') as f:
			json.dump(latest_commit, f, indent=4)
		print("New commit detected!")
		print(f"Latest commit message: {latest_commit['commit']['message']}")
		print(f"Latest commit author: {latest_commit['commit']['author']['name']}")
		print(f"Latest commit timestamp: {latest_commit['commit']['author']['date']}")
		print(f"Latest commit sha: {latest_commit['sha']}")
		bot = telegram.Bot(token=os.environ['botkey'])

		numbers = []
		with open('log.txt', 'r') as file:
		  for line in file:
		    user_id = int(line.split(',')[-1].split(')')[0].split(' ')[1])
		    numbers.append(int(user_id))
		unique_numbers = list(set(numbers))

		for u_chat_id in unique_numbers:
			try:
				text = latest_commit['commit']['message']
				title, desc = text.split('\n\n')
				bot.send_message(chat_id=u_chat_id, text=f"<b>Commit message [Changelogs]</b> \n<code>{title}</code>\n\n<b><b>{desc}</b></b>\n\n<b>Timestamp: </b>{latest_commit['commit']['author']['date']}", parse_mode='html')
			except:
				print(f"User {u_chat_id} has blocked the bot, message not sent.")
				continue