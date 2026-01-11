__title__ = "bot-formatter"
__author__ = "tibue99"
__license__ = "MIT"
__version__ = "0.1.1"


import sys

from bot_formatter.run import BotFormatter


def run():
    BotFormatter(sys.argv[1:])
