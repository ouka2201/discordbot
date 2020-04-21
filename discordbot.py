from discord.ext import tasks,commands
import os
import traceback
import random
import math
from asyncio import sleep
import datetime
import csv
import pandas as pd
import discord

CHANNEL_ID = 618007010071543809
bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']
player_list = []

@bot.event
async def regular_processing():
	while True:
		now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
		#name1, name2, time = nextpop(now.weekday(), now.hour, now.minute)
		name1, name2, time = nextpop(1, 10, 40)
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
					channel = bot.get_channel(CHANNEL_ID)
					await channel.send(embed=pop)
			except AttributeError:
				pass
			except TimeoutError:
				pass
	await sleep(60)

@bot.event
async def on_command_error(ctx, error):
	orig_error = getattr(error, "original", error)
	error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
	await ctx.send(error_msg)
								 
@bot.command()
async def ping(ctx):
	embed = discord.Embed(description="おはようございますぅ")
	embed.set_author(name="雅/Mashas.",icon_url="https://cdn.discordapp.com/attachments/562098530366390275/701668974114504745/442d2198c53f8e1d.png")
	await ctx.send(embed=embed)
    
@bot.command()
async def s (ctx,*args):
	player_list = list(args)
	random.shuffle(player_list)  
	n = math.ceil(len(player_list) / 2)
	date1 = player_list[:n]
	date2 = player_list[n:]
	bteam ='\n'.join(date1)
	oteam ='\n'.join(date2)

	keka = discord.Embed(title="「チーム分けの結果ですぅ」")
	keka.set_author(name="雅/Mashas.",icon_url="https://cdn.discordapp.com/attachments/562098530366390275/701668974114504745/442d2198c53f8e1d.png")
	keka.add_field(name="ブルーチームですぅ",value=bteam,inline=False)
	keka.add_field(name="オレンジチームですぅ",value=oteam,inline=False)
	keka.set_footer(text="「glhfですぅ」")

	await ctx.send(embed=keka)
    
@bot.command()
async def p (ctx,*args):
	name1,name2,time = nextpop(0,15,50)
	pop = discord.Embed(title="pop")
	pop.add_field(name="時間",value=time,inline=False)
	pop.add_field(name="一匹め",value=name1,inline=False)
	pop.add_field(name="二匹め",value=name2,inline=False)
	
	await ctx.send(embed=pop)
	
@bot.command()
async def t(ctx):
	channel = bot.get_channel(CHANNEL_ID)
	await channel.send("!!!!!")
	
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
	
bot.loop.create_task(regular_processing())
bot.run(token)
