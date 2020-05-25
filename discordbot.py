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
import cogs.audio as audio
import requests
import json
import mkjson
import textformat
from google.cloud import texttospeech


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
		return (f"各コマンドの説明: {prefix}help <コマンド名>\n"
			f"各カテゴリの説明: {prefix}help <カテゴリ名>\n"
			f"ミュートした状態でききせんチャットになにか打つとそれを話す。\n"
			f"会話用で話すと何かしら返してくれるよ！\n")

bot = commands.Bot(command_prefix=prefix, help_command=JapaneseHelpCommand())

@bot.event
async def on_ready():
	print("on_ready")
	print(discord.__version__)
	mashas.setup(bot)
	audio.setup(bot)
	
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
			text = textformat.format_text(message.content)
			if text == "":
				await message.channel.send("画像、絵文字やURLには反応できません;;")
				return
			response = requests.request("POST", url, data=mkjson.mkcplus(text, message.author.name), headers=headers)
			res = json.loads(response.text)
			await message.channel.send((res['bestResponse'])['utterance'])
	await bot.process_commands(message)
@bot.event
async def on_voice_state_update(member, before, after):
	if after.channel is None:
		if len(before.channel.members) == 1:
			await member.guild.voice_client.disconnect()

	if after.self_mute:
		# voicechannelを取得
		vc = after.channel
		print('------')
		# voicechannelに接続
		await vc.connect()
	
@bot.event
async def on_message(message):
	ch_name = "ききせん"
	if message.channel.name == ch_name:
		if message.content.startswith('/'):
			pass
		else:
			if message.author.voice.self_mute:
				if message.guild.voice_client:
					print(message.author.name)
					text = textformat.format_text(message.content)
					if text == "":
						print(text)
					else:
						txt = message.author.name + "のメッセージです。" + text
						makemp3(txt)
						source = discord.FFmpegPCMAudio("output.mp3")
						message.guild.voice_client.play(source)
				else:
					pass
	await bot.process_commands(message)
	
def makemp3(str):
	# クライアントの作成
	client = texttospeech.TextToSpeechClient()

	# 引数のテキストをセット
	synthesis_input = texttospeech.types.SynthesisInput(text=str)

	# ボイスのリクエスト nameを書き換えれば他の音声に変更可能
	voice = texttospeech.types.VoiceSelectionParams(
		language_code='ja-JP',
		name='ja-JP-Wavenet-A',
		ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

	# オーディオコンフィグ
	audio_config = texttospeech.types.AudioConfig(
		audio_encoding=texttospeech.enums.AudioEncoding.MP3,
		speaking_rate=1.8)

	# 色々まとめる
	response = client.synthesize_speech(synthesis_input, voice, audio_config)

	# バイナリ書き込み
	with open('output.mp3', 'wb') as out:
		out.write(response.audio_content)
		print('Audio content written to file "output.mp3"')
	
bot.run(token)
