import discord

from .. import PensionBot


class StopCog(discord.Cog):
    def __init__(self, pension_bot: PensionBot):
        self.pension_bot = pension_bot

    @discord.command()
    async def stop(self, context: discord.context.ApplicationContext):
        await self.pension_bot._voice_clients[context.author.id].disconnect()


def setup(pension_bot: PensionBot):
    pension_bot.add_cog(StopCog(pension_bot))
