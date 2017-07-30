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
7. redis-py

# TODO
1. Perhaps make the timer command a little simpler by breaking it up into functions
2. Come up with way to have bot auto leave voice if it is the only user. on_voice_state_update might be the right direction.
3. Spam message filter
  * Delete messages (option) if they exceed a certain number in X seconds
  * Delete message as it comes in if the rate is limited
4. Allow different chain lengths for markov (low priority, high memory usage potential)
5. Store settings and reactions as json/yaml instead of pickle
  * Pickle isn't easy to manually edit if you wanted to
  * 5.1 Write script to automatically merge old and new settings files so that if new settings are added, they get put into the server's file