__title__ = "ezbot"
__author__ = "tibue99"
__license__ = "MIT"
__version__ = "0.0.1"


import sys

from ezbot.run import EzBot


def run():
    EzBot(sys.argv[1:])
