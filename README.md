# DiscordBot
Discord bot written with Discord.py

# Setup
You may need to create a `logs` directory in the application root. This will hold the message logs for the markov fuctionality. Each server's messages are stored in their own file.
You may also need to create a `data` directory in the application root. This will hold information about each server's settings and reactions.

Configure a config.yaml based on the example.

# Requirements
1. Python 3.6+
2. Discord.py python library
3. PyYAML python library
4. youtube_dl python library
5. Opus Library
6. ffmpeg

# TODO
1. Move the commands to a new file
2. Perhaps make the timer command a little simpler by breaking it up into functions
3. Allow moderators in servers to customize markovSentenceLength and markovDigestLength
4. Come up with way to have bot auto leave voice if it is the only user. on_voice_state_update might be the right direction.
5. Enable/Disable image reactions
6. Allow moderators in servers to change probability of reactions (serialize data and store to DB/file)
7. Allow moderators in servers to add/remove reactions (serialize data and store to DB/file)
8. Come up with a way to store default reactions for a server.
9. Spam message filter
  * Use redis to monitor number of messages a user has sent in X seconds
  * Delete messages (option) if they exceed a certain number in X seconds
10. Spam prevention
  * Place user into timeout group that doesn't allow messages to be sent (option) if they spam
  * Message moderators/admins
