import discord

from .. import PensionBot


class PlayCog(discord.Cog):
    def __init__(self, pension_bot: PensionBot):
        self.pension_bot = pension_bot

    @discord.command()
    async def play(
        self,
        context: discord.context.ApplicationContext,
        name: discord.Option(discord.SlashCommandOptionType.string),  # type: ignore
    ):
        station = self.pension_bot.radio_browser_api.search(name)

        author = context.author
        voice = author.voice

        if not voice:
            return

        voice_client = await voice.channel.connect()
        voice_client.play(discord.FFmpegOpusAudio(station.url, executable="bin/ffmpeg"))

        self.pension_bot._voice_clients[author.id] = voice_client

        embed = discord.Embed(
            description=f"Сейчас играет `{station.name}`", thumbnail=station.favicon
        )

        await context.respond(embed=embed)


def setup(pension_bot: PensionBot):
    pension_bot.add_cog(PlayCog(pension_bot))
