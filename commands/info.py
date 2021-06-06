import json
import discord
import settings
import datetime
import dateutil.parser

from utils import get_emoji
from commands.base_command      import BaseCommand
from commands.mongo_connection import connect


db = connect()
db_col = db['users']
db_col_events = db['events']

def toTimestamp(datetime_str):
    return dateutil.parser.parse(datetime_str, dayfirst=True).timestamp()

def toDateTimeObj(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%A %d %Y')



class Info(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Returns user's info."
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = None
        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # 'params' is a list that contains the parameters that the command
        # expects to receive, t is guaranteed to have AT LEAST as many
        # parameters as specified in __init__
        # 'message' is the discord.py Message object for the command to handle
        # 'client' is the bot Client object

        calender_emoji = get_emoji('calendar')
        scroll_emoji = get_emoji('scroll')
        briefcase_emoji = get_emoji('briefcase')
        redcircle_emoji = get_emoji('red_circle')

        author_name = str(message.author).split('#')[0]
        author_tag = str(message.author).split('#')[1]
        query = db_col.find({'discord_name' : f'{author_name}', 'discord_tag' : f'{author_tag}'})
        info = [x for x in query]
        if not info:
            await message.channel.send("You need to register first.")
        else:

            roles = ''

            if not info[0]['codes_used']:
                workshops_attended = 'No workshops attended'
            else:
                workshops_attended = ''
                for code in info[0]['codes_used']:
                    query = db_col_events.find({'code' : code})
                    workshop_info = [x for x in query]
                    workshops_attended += '\n' + workshop_info[0]['workshop_name']


            for role in message.author.roles:
                roles += f', @{role}'


            embed = discord.Embed(title=f"{redcircle_emoji} {str(message.author)} Info:\r\n\u200B", color=0x69E4BE)
            embed.add_field(name=f"{calender_emoji} Registration Date:", value=f'{toDateTimeObj(toTimestamp(info[0]["timestamp"]))}\n\u200B',  inline=False)
            embed.add_field(name=f"{briefcase_emoji} Roles:", value=roles[3:] + f"\n\u200B",  inline=False)
            embed.add_field(name=f"{scroll_emoji} Workshops Attended :", value=workshops_attended)
            await message.channel.send(embed=embed)
