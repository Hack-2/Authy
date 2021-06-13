import json
import discord
import settings
import datetime
import dateutil.parser

from utils import get_emoji
from commands.base_command      import BaseCommand
from commands.mongo_connection import connect


class Purge(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Deletes all messages in a channel."
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

        roles = [(x.name).lower() for x in message.author.roles]
        if 'organizer' in roles:
            await message.channel.purge(limit=50*100)
            await message.channel.send(f'{message.author.mention} Deleted all messages in this channel.', delete_after=5*60)
        else:
            await message.channel.send(f'{message.author.mention} You don\'t have access to use this command.', delete_after=5*60)
