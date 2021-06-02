import os
import json


with open('.env', 'r') as f:
    env = json.load(f)

# The prefix that will be used to parse commands.
# It doesn't have to be a single character!
COMMAND_PREFIX = "!"

# The bot token. Keep this secret!
BOT_TOKEN = env['token']

# The now playing game. Set this to anything false-y ("", None) to disable it
NOW_PLAYING = COMMAND_PREFIX + "commands"

# Base directory. Feel free to use it if you want.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

#Mongo db credentials
mongodb_user = env['mongodb_user']
mongodb_pass = env['mongodb_pass']
