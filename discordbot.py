from discord.ext import tasks,commands
import os
import traceback
from asyncio import sleep
import random
import math
from googletrans import Translator
import datetime
import pandas as pd
import discord
import cogs.mashas as mashas
import requests
import json
import mkjson


token = os.environ['DISCORD_BOT_TOKEN']
apikey = os.environ['ART_API_KEY']
prefix = '-'

class JapaneseHelpCommand(commands.DefaultHelpCommand):
	def __init__(self):
		super().__init__()
		self.commands_heading = "コマンド:"
		self.no_category = "その他"
		self.command_attrs["help"] = "コマンド一覧と簡単な説明を表示"
	def get_ending_note(self):
		return (f"各コマンドの説明: {prefix}help <コマンド名>\n"f"各カテゴリの説明: {prefix}help <カテゴリ名>\n"f"会話用で話すと何かしら返してくれるよ！\n")

bot = commands.Bot(command_prefix=prefix, help_command=JapaneseHelpCommand())

@bot.event
async def on_ready():
	print("on_ready")
	print(discord.__version__)
	mashas.setup(bot)
	
@bot.event
async def on_message(message):
	ch_name = "会話用"
	if message.channel.name == ch_name:
		if message.author.bot:
			return
		if message.content.startswith('/'):
			return
		if message.content.startswith('-'):
			return
		else:
			url = "https://www.chaplus.jp/v1/chat?apikey=" + apikey
			headers = {'content-type': "application/json"}
			response = requests.request("POST", url, data=mkjson.mkcplus(message.content, message.author.name), headers=headers)
			res = json.loads(response.text)
			await message.channel.send((res['bestResponse'])['utterance'])
	await bot.process_commands(message)
			
bot.loop.create_task(regular_processing())
bot.run(token)
