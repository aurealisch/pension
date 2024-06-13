import discord

from .. import PensionBot


class OnVoiceStateUpdateCog(discord.Cog):
    def __init__(self, pension_bot: PensionBot):
        self.pension_bot = pension_bot

    @discord.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        if member.bot:
            return

        if before.channel is not None and after.channel is None:
            await self.pension_bot._voice_clients[member.id].disconnect()


def setup(pension_bot: PensionBot):
    pension_bot.add_cog(OnVoiceStateUpdateCog(pension_bot))
