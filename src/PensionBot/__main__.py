import dotenv

from . import PensionBot
from .modules.radio_browser_api import RadioBrowserAPI

pension_bot = PensionBot(RadioBrowserAPI())
dotenv.load_dotenv()
pension_bot.run()
