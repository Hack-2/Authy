import discord
import datetime
import dateutil.parser
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


from commands.mongo_connection import connect
from events.base_event         import BaseEvent
from utils                     import get_channel



db = connect()
db_col = db['users']


def toTimestamp(datetime_str):
    return dateutil.parser.parse(datetime_str, dayfirst=True).timestamp()

def toDateTimeObj(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')




# Matplotlib graphs under development.
class plot(BaseEvent):

    def __init__(self):
        interval_minutes = 1440  # Set the interval for this event
        super().__init__(interval_minutes)

    # Override the run() method
    # It will be called once every {interval_minutes} minutes
    async def run(self, client):
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

        plt.xticks(rotation=22)
        plt.plot(*zip(*sorted(allDates.items())), color='#388CF7')
        plt.xlabel("Time")
        plt.ylabel("Users")
        plt.savefig('tmp.png', bbox_inches='tight')
        plt.close()


        file = discord.File('tmp.png')
        embed = discord.Embed(title='Users Plot', color=0x69E4BE)
        embed.set_image(url="attachment://tmp.png")
        channel = get_channel(client, "logs")
        await channel.send(embed=embed, file=file)
