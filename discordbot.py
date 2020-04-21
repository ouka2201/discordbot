from discord.ext import tasks,commands
import os
import traceback
import random
import math
from asyncio import sleep
import datetime
import pandas as pd
import discord
from googletrans import Translator

bot = commands.Bot(command_prefix='-')
token = os.environ['DISCORD_BOT_TOKEN']
player_list = []
translator = Translator()

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

@bot.command(name="占い")
async def uranai(ctx):
	lucks = ["大吉", "中吉", "小吉", "吉", "凶", "大凶"]
	luck = random.choice(lucks)

	# 運勢の内容で表示する文章を変える
	if luck == "大吉" or luck == "中吉":
		detail = "いい事あるといいですねぇ"
	elif luck == "小吉" or luck == "吉":
		detail = "中途半端ですねぇ"
	else:
		detail = "死んでください"

	keka = discord.Embed(title="「今日の運勢ですぅ」")
	keka.set_author(name="雅/Mashas.",icon_url="https://cdn.discordapp.com/attachments/562098530366390275/701668974114504745/442d2198c53f8e1d.png")
	keka.add_field(name="占いの結果", value=luck, inline=False)
	keka.set_footer(text=detail)

	await ctx.send(embed=keka)

@bot.command()
async def p (ctx,*args):
	now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
	name1, name2, time = nextpop(now.weekday(), now.hour, now.minute)
	pop = discord.Embed(title="pop")
	pop.add_field(name="時間",value=time,inline=False)
	pop.add_field(name="一匹め",value=name1,inline=False)
	pop.add_field(name="二匹め",value=name2,inline=False)
	
	await ctx.send(embed=pop)
@bot.command(name="t")
async def trans(ctx, *, arg):
	str = arg
	detect = translator.detect(str)
	befor_lang = detect.lang
	if befor_lang == 'ja':
		convert_string = translator.translate(str, src=befor_lang, dest='en')
		embed = discord.Embed(title='「翻訳結果ですぅ」', color=0xff0000)
		embed.set_author(name="雅/Mashas.", icon_url="https://cdn.discordapp.com/attachments/562098530366390275/701668974114504745/442d2198c53f8e1d.png")
		embed.add_field(name='Befor', value=str)
		embed.add_field(name='After', value=convert_string.text, inline=False)
		embed.set_footer(text="いかがですか？？？")
		
		await ctx.send(embed=embed)
	else:
		convert_string = translator.translate(str, src=befor_lang, dest='ja')
		embed = discord.Embed(title='「翻訳結果ですぅ」', color=0xff0000)
		embed.set_author(name="雅/Mashas.",icon_url="https://cdn.discordapp.com/attachments/562098530366390275/701668974114504745/442d2198c53f8e1d.png")
		embed.add_field(name='Befor', value=str)
		embed.add_field(name='After', value=convert_string.text, inline=False)
		embed.set_footer(text="いかがですか？？？")
		
		await ctx.send(embed=embed)

@bot.command(name="d")
async def detectbot(ctx, *, arg):
	detect = translator.detect(arg)
	m = detect.lang + ' ですぅ'
	embed = discord.Embed(title="「言語解析結果ですぅ」")
	embed.set_author(name="雅/Mashas.", icon_url="https://cdn.discordapp.com/attachments/562098530366390275/701668974114504745/442d2198c53f8e1d.png")
	embed.add_field(name="この言語はおそらく", value=m, inline=False)
	embed.set_footer(text="いかがですか？？？")
	
	await ctx.send(embed=embed)
	
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
