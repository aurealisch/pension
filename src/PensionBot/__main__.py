import dotenv

from . import PensionBot
from .modules.radio_browser_api import RadioBrowserAPI

dotenv.load_dotenv()
PensionBot(RadioBrowserAPI()).run()
