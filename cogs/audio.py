from discord.ext import commands
import discord
import random
import math
from googletrans import Translator

class audio(commands.Cog, name='読み上げ'):
  def __init__(self, bot):
    super().__init__()
    self.bot = bot
        
@commands.command(name="join")
async def join(self, ctx):
  """botがチャンネルに接続する"""
  # voicechannelを取得
  vc = ctx.author.voice.channel
  # voicechannelに接続
  await vc.connect()

@commands.command(name="bye")
async def bye(self, ctx):
  """botが切断"""
  # 切断
  await ctx.voice_client.disconnect()

def setup(bot):
  print("起動")
  bot.add_cog(audio(bot))
