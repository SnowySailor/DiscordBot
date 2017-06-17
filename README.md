# DiscordBot
Discord bot written with Discord.py

# Setup
You may need to create a `logs` directory in the application root. This will hold the message logs for the markov fuctionality. Each server's messages are stored in their own file.

Configure a config.yaml based on the example.

# TODO
1. When reading in data, count the bytes as it is read in order to truly maximize the number of lines read in while still being under the max_bytes limit. If we are only reading in messages longer than 15 words, but we also have messages that are 5 words, we don't want to "use up" data with the 5 word messages. Use len(string.encode('utf-8')) to get byte length.
2. Move the commands to a new file
3. Perhaps make the timer command a little simpler by breaking it up into functions