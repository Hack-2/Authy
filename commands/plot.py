import discord
import settings
import datetime
import dateutil.parser
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from utils                      import get_channel
from commands.base_command      import BaseCommand
from commands.mongo_connection import connect


db = connect()
db_col = db['users']

def toTimestamp(datetime_str):
    return dateutil.parser.parse(datetime_str, dayfirst=True).timestamp()

def toDateTimeObj(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')



class Plot(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Plots the increase of users with time."
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
            dates = []
            for user in db_col.find():
                timestamp = toDateTimeObj(toTimestamp(user['timestamp']))
                dates.append(timestamp)

            occ = [0 for x in range(len(dates))]

            startDate = datetime.datetime.strptime( dates[0], "%Y-%m-%d")
            endDate   = datetime.datetime.strptime( dates[-1],"%Y-%m-%d")
            days = (endDate - startDate).days

            allDates = {datetime.datetime.strftime(startDate+datetime.timedelta(days=k),
                                               "%Y-%m-%d"):0 for k in range(days+1)}

            allDates.update(zip(dates,occ))
            datesAfter,occAfter = map(list,zip(*sorted(allDates.items())))
            dates_to_delete = datesAfter[0:-5]
            for x in dates_to_delete:
                allDates.pop(x)

            for date in dates:
                if date in allDates:
                    allDates[date] = allDates[date] + 1

            plt.plot(*zip(*sorted(allDates.items())), color='#388CF7')
            plt.xlabel("Time")
            plt.ylabel("Users")
            plt.savefig('tmp.png', bbox_inches='tight')
            plt.close()


            file = discord.File('tmp.png')
            embed = discord.Embed(title='Users Plot', color=0x69E4BE)
            embed.set_image(url="attachment://tmp.png")
            channel = client.get_channel(settings.test_server_logs_id)
            await channel.send(embed=embed, file=file)
        else:
            await message.channel.send(f'{message.author.mention} You don\'t have access to use this command.', delete_after=5*60)
