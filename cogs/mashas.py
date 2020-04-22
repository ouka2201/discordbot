from discord.ext import commands
import random
import math
from googletrans import Translator

player_list = []
translator = Translator()

class mashas(commands.Cog, name='便利系'):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    @commands.command()
    async def ping(self, ctx):
        """まこんが挨拶するだけ"""
        embed = discord.Embed(description="おはようございますぅ")
        embed.set_author(name="雅/Mashas.",icon_url="https://cdn.discordapp.com/attachments/562098530366390275/701668974114504745/442d2198c53f8e1d.png")

        await ctx.send(embed=embed)

    @commands.command()
    async def s (self, ctx,*args):
        """空白入れながら名前書いてくと分けてくれる"""
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

    @commands.command(name="占い")
    async def uranai(self, ctx):
        """占うやつ"""
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

    @commands.command(name="t")
    async def trans(self, ctx, *, arg):
        """まこんが翻訳してくれる"""
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

    @commands.command(self, name="d")
    async def detectbot(ctx, *, arg):
        """まこんが何語か解説してくれる"""
        detect = translator.detect(arg)
        m = detect.lang + ' ですぅ'
        embed = discord.Embed(title="「言語解析結果ですぅ」")
        embed.set_author(name="雅/Mashas.", icon_url="https://cdn.discordapp.com/attachments/562098530366390275/701668974114504745/442d2198c53f8e1d.png")
        embed.add_field(name="この言語はおそらく", value=m, inline=False)
        embed.set_footer(text="いかがですか？？？")

        await ctx.send(embed=embed)

def setup(bot):
    print("起動")
    bot.add_cog(mashas(bot))
