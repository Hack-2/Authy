import discord
import json

from models import verifyCode

client = discord.Client()

with open('.env', 'r') as file:  
    TOKEN = json.load(file)
    TOKEN = TOKEN['token']

commands = []  # Initialize commands

channel = 'testing'

class Command:
    def __init__(self, command, channel, output):
        self.command = command
        self.channel = channel
        self.output = output
        commands.append(self)  # Add command to commands list

    def run(self):
        if self.command == '.verify':
            pong()

        return self.output



# Add commands below
Command('.verify', channel, 'Verified your code.')


@client.event
async def on_message(message):
    message_ = message.content.split()
    for command in commands:
        if len(message_) > 1 and message_[0] == command.command and str(message.channel) == command.channel and message_[1][0] == '#' and len(message_) == 2:
            # msg = command.run()
            # msg = msg.format(message)
            author = str(message.author).split('#')
            response = verifyCode(author[0], author[1], message_[1])
            await message.channel.send(response)
        else:
            pass


async def ready():
    await client.wait_until_ready()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="your commands!"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.loop.create_task(ready())
client.run(TOKEN)
