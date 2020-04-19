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
CHANNEL = discord.Object(id=CHANNEL_ID)




@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    embed = discord.Embed(title="Embedのタイトル",description="Embedの概要")
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
        
    await ctx.send("```【BlueTeam】\n"+ str(bteam)+"```"+"\n```【OrangeTeam】\n"+ str(oteam)+"```")
    
    
bot.run(token)
