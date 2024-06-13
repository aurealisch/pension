import discord

from .. import PensionBot
from ..exceptions import NotConnectedException
from ..modules.radio_browser_api import Station


class SelectStation(discord.ui.Select):
    def __init__(self, stations: list[Station], pension_bot: PensionBot) -> None:
        options = map(
            lambda station: discord.SelectOption(
                label=station.name, value=station.stationuuid
            ),
            stations,
        )
        super().__init__(placeholder="Select a station", options=options)
        self.stations = stations
        self.pension_bot = pension_bot

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        user_id = user.id
        user_voice = user.voice

        if not user_voice:
            raise NotConnectedException

        stations_uuids = {station.stationuuid: station for station in self.stations}
        station = stations_uuids[self.values[0]]

        voice_clients = self.pension_bot._voice_clients

        if user_id in voice_clients:
            voice_client = voice_clients[user_id]
            voice_client.stop()
        else:
            voice_client = await user_voice.channel.connect()
            voice_clients[user_id] = voice_client

        voice_client.play(discord.FFmpegOpusAudio(station.url, executable="bin/ffmpeg"))

        await interaction.response.edit_message(
            embed=discord.Embed(
                description=f"Now playing: **`{station.name}`**",
            ),
        )


class PlayCog(discord.Cog):
    def __init__(self, pension_bot: PensionBot):
        self.pension_bot = pension_bot

    @discord.command()
    async def play(
        self,
        context: discord.context.ApplicationContext,
        name: discord.Option(discord.SlashCommandOptionType.string),  # type: ignore
    ):
        pension_bot = self.pension_bot
        stations = pension_bot.radio_browser_api.search(name)

        await context.respond(
            view=discord.ui.View(SelectStation(stations, pension_bot))
        )


def setup(pension_bot: PensionBot):
    pension_bot.add_cog(PlayCog(pension_bot))
