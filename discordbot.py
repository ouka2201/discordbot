from discord.ext import commands
import os
import traceback
import random
import math

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
    await ctx.send('pong')
    
@bot.command()
async def add (ctx,*args):
    player_list = list(args)
    random.shuffle(player_list)  
    n = math.ceil(len(player_list) / 2)
    date1 = player_list[:n]
    date2 = player_list[n:]
    bteam ='\n'.join(date1)
    oteam ='\n'.join(date2)
        
    await ctx.send("【BlueTeam】"+ str(bteam)+ str(oteam))
    
    
bot.run(token)
