import os

import discord

from .modules.radio_browser_api import RadioBrowserAPI


class PensionBot(discord.Bot):
    def __init__(self, radio_browser_api: RadioBrowserAPI):
        super().__init__()
        self.radio_browser_api = radio_browser_api
        self._voice_clients: dict[str, discord.VoiceClient] = {}

    def run(self) -> None:
        for cog in ["play", "stop", "on_voice_state_update"]:
            self.load_extension(f"src.PensionBot.cogs.{cog}")

        return super().run(os.getenv("PENSION_BOT_TOKEN"))
