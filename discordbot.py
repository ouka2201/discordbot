from discord.ext import tasks,commands
import os
import traceback
from asyncio import sleep
import datetime
import pandas as pd
import discord
import pya3rt
import cogs.mashas as mashas

token = os.environ['DISCORD_BOT_TOKEN']
apikey = os.environ['ART_API_KEY']
pyart = pya3rt.TalkClient(apikey)
player_list = []
translator = Translator()
prefix = '-'

class JapaneseHelpCommand(commands.DefaultHelpCommand):
	def __init__(self):
		super().__init__()
		self.commands_heading = "コマンド:"
		self.no_category = "その他"
		self.command_attrs["help"] = "コマンド一覧と簡単な説明を表示"
	def get_ending_note(self):
		return (f"各コマンドの説明: {prefix}help <コマンド名>\n"f"各カテゴリの説明: {prefix}help <カテゴリ名>\n")

bot = commands.Bot(command_prefix=prefix, help_command=JapaneseHelpCommand())

@bot.event
async def on_ready():
	print("on_ready")
	print(discord.__version__)
	mashas.setup(bot)

@bot.event
async def regular_processing():
	while True:
		now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
		name1, name2, time = nextpop(now.weekday(), now.hour, now.minute)
		if name1 is None:
			print("...")
		else:
			try:
				res1 = name1 + "が出現します！"
				if name2 == "いないよ":
					res2 = "二匹目は存在しません!"
				else:
					res2 = name2 + "が出現します！"
				res3 = time + "より"
				pop = discord.Embed(title="ワールドボス20分前通知")
				pop.add_field(name="時間", value=res3, inline=False)
				pop.add_field(name="出現ワールドボス１", value=res1, inline=False)
				pop.add_field(name="出現ワールドボス２", value=res2, inline=False)
				ch_name = "通知"
				for channel in bot.get_all_channels():
					if channel.name == ch_name:
						await channel.send(embed=pop)
			except AttributeError:
				pass
			except TimeoutError:
				pass
			
		await sleep(60)
	
def nextpop(wday,hour,min):
	df = pd.read_csv("pop.csv", index_col=0)
	df.query('wday == @wday & hour == @hour & min == @min', inplace=True)
	if df.empty:
		return None,None,None
	else:
		name1 = df['name1'].values[0]
		name2 = df['name2'].values[0]
		time = df['time'].values[0]
		return name1,name2,time
	
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
			response = pyart.talk(message.content)
			await message.channel.send(((response['results'])[0])['reply'])
	await bot.process_commands(message)
			
bot.loop.create_task(regular_processing())
bot.run(token)
