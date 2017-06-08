import re
import random
from markovgen import Markov

#Function to handle messages. Uses the regex library to match certian situations.
#Randomness is to keep the bot from spamming
async def handle(msg, bot, client):
	if re.match("spicy", msg.content, re.IGNORECASE):
		s = random.randint(0,2)
		if(s == 1):
			await client.send_message(msg.channel, "http://i.imgur.com/l50LNcp.jpg")
			return

	if re.match("obama", msg.content, re.IGNORECASE):
		s = random.randint(0,1)
		if(s == 1):
			await client.send_message(msg.channel, "http://imgur.com/WVwEZ1b.jpg")
			return

	if re.match("disappoint", msg.content, re.IGNORECASE):
		s = random.randint(0,2)
		if(s == 1):
			await client.send_message(msg.channel, "http://imgur.com/TfT8wvi.gif")
			return

	if re.match("((you.? ?r?(ar)?e)|your) wrong", msg.content, re.IGNORECASE):
		s = random.randint(0,1)
		if(s == 1):
			await client.send_message(msg.channel, "http://imgur.com/VrM58GT.jpg")
			return

	if re.match("obligations", msg.content, re.IGNORECASE):
		s = random.randint(0,2)
		if(s == 1):
			await client.send_message(msg.channel, "http://i.imgur.com/rbJTvlf.jpg")
			return

	if re.match("^(hi|hello) (waifu|bot) ?(bot)?", msg.content, re.IGNORECASE):
		await client.send_message(msg.channel, "Hi {0.author.mention}".format(msg))
		return

	if re.match("^(grr)(\s|.)?", msg.content, re.IGNORECASE):
		s = random.randint(0,4)
		if(s == 1):
			await client.send_message(msg.channel, "http://i.imgur.com/FH7f5Ta.gif")
		if(s == 2):
			await client.send_message(msg.channel, "_me pats you on the head_")
		return

	if re.match("^bot be random", msg.content, re.IGNORECASE):
		if not getattr(bot, 'markov', None):
			await client.send_message(msg.channel, "Loading data.")
			with open("/tmp/chat.txt","r", encoding='utf-8', errors='ignore') as f:
				bot.markov = Markov(f)
		text = bot.markov.generate_markov_text(random.randint(6,40))
		await client.send_message(msg.channel, text)
		return
	return