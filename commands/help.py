import discord
from commands.base_command import BaseCommand

from utils import get_emoji


# This is a convenient command that automatically generates a helpful
# message showing all available commands
class Help(BaseCommand):

    def __init__(self):
        description = "Displays this help message"
        params = None
        super().__init__(description, params)

    async def handle(self, params, message, client):
        from message_handler import COMMAND_HANDLERS
        books_emoji = get_emoji('books')
        embed = discord.Embed(title=f"{books_emoji} Hacky-Auth Commands:\n\u200B", color=0x32a89e)

        # Displays all descriptions, sorted alphabetically by command name
        roles = [(x.name).lower() for x in message.author.roles]
        for cmd in sorted(COMMAND_HANDLERS.items()):
            name  = cmd[1].description.split(':')[0]
            value = cmd[1].description.split(':')[1]
            embed.add_field(name=name, value=value,  inline=False)

        await message.channel.send(embed=embed)
