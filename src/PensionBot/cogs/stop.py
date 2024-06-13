import discord

from .. import PensionBot
from ..exceptions import NotConnectedException


class StopCog(discord.Cog):
    def __init__(self, pension_bot: PensionBot):
        self.pension_bot = pension_bot

    @discord.command()
    async def stop(self, context: discord.context.ApplicationContext):
        author = context.author
        voice = author.voice

        if not voice:
            raise NotConnectedException

        await self.pension_bot._voice_clients[author.id].disconnect()
        await context.respond(embed=discord.Embed(description="Stopped"))


def setup(pension_bot: PensionBot):
    pension_bot.add_cog(StopCog(pension_bot))
