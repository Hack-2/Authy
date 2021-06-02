import discord
from commands.base_command import BaseCommand


# This is a convenient command that automatically generates a helpful
# message showing all available commands
class Help(BaseCommand):

    def __init__(self):
        description = "Displays this help message"
        params = None
        super().__init__(description, params)

    async def handle(self, params, message, client):
        from message_handler import COMMAND_HANDLERS

        embed = discord.Embed(title="Hacky-Auth Commands:", color=0x32a89e)

        # Displays all descriptions, sorted alphabetically by command name
        for cmd in sorted(COMMAND_HANDLERS.items()):
            name  = cmd[1].description.split(':')[0]
            value = cmd[1].description.split(':')[1]
            embed.add_field(name=name, value=value,  inline=False)

        await message.channel.send(embed=embed)
