import discord
from discord.ext import commands
from __main__ import send_cmd_help
import os
from os import listdir
from os.path import isfile, join
import string


class emo:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
        self.local_emo_static_path = "data/emos/static/vampy"
        self.local_emo_custom_path = "data/emos/static/custom"
        self.local_emo_gif_path= "data/emos/gif"

    def _list_emo(self):
        ret = []
        for thing in listdir(self.local_emo_static_path):
            if isfile(os.path.join(self.local_emo_static_path, thing)):
                ret.append(thing.split(".")[0])
        return ret

    def _list_emo_custom(self):
        ret = []
        for thing in listdir(self.local_emo_custom_path):
            if isfile(os.path.join(self.local_emo_custom_path, thing)):
                ret.append(thing.split(".")[0])
        return ret

    def _list_emo_gif(self):
        ret = []
        for thing in listdir(self.local_emo_gif_path):
            if isfile(os.path.join(self.local_emo_gif_path, thing)):
                ret.append(thing.split(".")[0])
        return ret

    def _get_emo(self, emoName):
        lists = self._list_emo()
        lists2 = self._list_emo_custom()
        if emoName in lists:
            url = self.local_emo_static_path+ "/" + emoName + '.png'
            return url
        if emoName in lists2:
            url = self.local_emo_custom_path+ "/" + emoName +'.png'
            return url
        else:
            return 0

    def _get_emo_gif(self, emoName):
        lists = self._list_emo_gif()
        if emoName in lists:
            url = self.local_emo_gif_path+ "/" + emoName + '.gif'
            return url
        else:
            return 0

    @commands.command(name="emo", pass_context=True)
    async def emo(self, ctx, emo):
        """Post emo from local!"""
        channel = ctx.message.channel
        urlEmo = self._get_emo(emo)
        if urlEmo == 0:
            await self.bot.say("Can't find this emo")
        else:
            await self.bot.send_file(channel, urlEmo)

    @commands.command(name="gifEmo", pass_context=True)
    async def gifEmo(self, ctx, emo):
        """Post gif emo from local!"""
        channel = ctx.message.channel
        urlEmo = self._get_emo_gif(emo)
        if urlEmo == 0:
            await self.bot.say("Can't find this emo")
        else:
            await self.bot.send_file(channel, urlEmo)

    @commands.command(name="listEmo", pass_context=True)
    async def listEmo(self, ctx):
        """List available emos!"""
        emoLists = self._list_emo()
        emoInfo = []
        emoCustomList = self._list_emo_custom()
        emoCustomInfo = []
        msg = ""
        msg2 = ""
        emoCustomTxt = ""
        for item in emoLists:
            emoInfo.append(item)
        for item in emoCustomList:
            emoCustomInfo.append(item)
        half = len(emoInfo)/2
        emoInfo1 = emoInfo[:int(half)]
        emoInfo2 = emoInfo[int(half):]
        msg += "\n".join(emoInfo1)
        msg2 += "\n".join(emoInfo2)
        emoCustomTxt += "\n".join(emoCustomInfo)
        em = discord.Embed(color=0xaa550f, title="Full Available Emo")
        em.add_field(name="Vampy Emo", value=msg)
        em.add_field(name="Vampy Emo", value=msg2)
        em.add_field(name="Custom Emo", value=emoCustomTxt)
        await self.bot.say(content = None, embed=em)

    @commands.command(name="listGifEmo", pass_context=True)
    async def listGifEmo(self, ctx):
        """List available gif emos!"""
        emoLists = self._list_emo_gif()
        emoInfo = []
        msg = ""
        for item in emoLists:
            emoInfo.append(item)
        msg += "\n".join(emoInfo)
        await self.bot.say(msg)

def setup(bot):
    bot.add_cog(emo(bot))