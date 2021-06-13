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
mongodb_user = env['mongo_user']
mongodb_pass = env['mongo_pass']


#Log channel ids
test_server_logs_id = 849556415056183296
main_server_logs_id = 850787339596464198
