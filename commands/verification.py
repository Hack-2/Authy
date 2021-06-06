import json
import settings


from utils                      import get_channel, get_emoji
from commands.base_command      import BaseCommand
from commands.mongo_connection import connect


db = connect()
db_col = db['users']
db_col_events = db['events']



class Verify(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Verifies workshop codes"
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["#WORKSHOP_CODE"]
        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # 'params' is a list that contains the parameters that the command
        # expects to receive, t is guaranteed to have AT LEAST as many
        # parameters as specified in __init__
        # 'message' is the discord.py Message object for the command to handle
        # 'client' is the bot Client object
        checkmark_emoji = get_emoji('white_check_mark')
        code = params[0]
        author_name = str(message.author).split('#')[0]
        author_tag = str(message.author).split('#')[1]
        event_codes = [x['code'] for x in db_col_events.find()]
        query = db_col.find({'discord_name' : f'{author_name}', 'discord_tag' : f'{author_tag}'})
        unique = [x for x in query]
        if not unique:
            msg = 'User not found, Please register first here: https://vtvktlsmrhk.typeform.com/to/H9gU9j6L.'
        else:
            if code in event_codes:
                _codes_used = []
                codes_used = unique[0]['codes_used']
                if not codes_used:
                    _codes_used.append(code)
                    db_col.update({"discord_name" : f"{author_name}", "discord_tag" : f"{author_tag}"}, {"$set" : {"codes_used" : _codes_used, "workshops_attended" : len(_codes_used)}})
                    msg = f'Verified code {checkmark_emoji}.'
                else:
                    if code not in unique[0]['codes_used']:
                        _codes_used = unique[0]['codes_used']
                        _codes_used.append(code)
                        db_col.update({"discord_name" : f"{author_name}", "discord_tag" : f"{author_tag}"}, {"$set" : {"codes_used" :_codes_used, "workshops_attended" : len(_codes_used)}})
                        msg = f'Verified code {checkmark_emoji}.'
                    else:
                        msg = 'Code already redeemed.'
            else:
                msg = 'Invalid code.'

        await message.channel.send(f'{message.author.mention} {msg}')
