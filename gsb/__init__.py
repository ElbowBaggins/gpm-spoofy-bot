from os import getenv
from .bot import GsbClient

GsbClient.TOKEN = getenv('DISCORD_BOT_TOKEN')
