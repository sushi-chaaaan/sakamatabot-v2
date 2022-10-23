import discord
from discord.ext import commands

from tools.io import read_yaml

class MyBot(commands.Bot):
    def __init__(self):
        self.load_config()
        pass

    def load_config(self):
        yum = read_yaml(r"config/config.yaml")
        self.env = yum["environment"]

    def run(self):

