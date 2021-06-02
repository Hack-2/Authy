import json
import discord
import settings

from commands.base_command      import BaseCommand
from commands.mongo_connection import connect


db = connect()
db_col = db['users']
db_col_events = db['events']


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
        author_name = str(message.author).split('#')[0]
        author_tag = str(message.author).split('#')[1]
        query = db_col.find({'discord_name' : f'{author_name}', 'discord_tag' : f'{author_tag}'})
        info = [x for x in query]

        workshops_attended = ''
        roles = ''

        for code in info[0]['codes_used']:
            query = db_col_events.find({'code' : code})
            workshop_info = [x for x in query]
            workshops_attended += '\n      ' + workshop_info[0]['workshop_name']

        for role in message.author.roles:
            roles += f', @{role}'



        embed = discord.Embed(title=f"{str(message.author)} Info:", color=0x32a89e)
        embed.add_field(name="Registration Date:", value=info[0]['registration_datetime'],  inline=False)
        embed.add_field(name="Roles:", value=roles.replace('@everyone', '')[5:],  inline=False)
        embed.add_field(name="Workshops Attended:", value=workshops_attended)
        await message.channel.send(embed=embed)
