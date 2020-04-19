from discord.ext import commands
import os
import traceback
import random
import math
from asyncio import sleep
import configparser
import datetime
import json
import re
import discord
import time_checker


bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']
player_list = []

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    embed = discord.Embed(description="おはようございますぅ")
    embed.set_author(name="雅/Mashas.",icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
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
    keka.set_author(name="雅/Mashas.",icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    keka.add_field(name="ブルーチームですぅ",value=bteam,inline=False)
    keka.add_field(name="オレンジチームですぅ",value=oteam,inline=False)
    keka.set_footer(text="「glhfですぅ」")
        
    await ctx.send(embed=keka)
    
    
bot.run(token)
