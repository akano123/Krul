import requests
import discord
import sys
sys.path.append('C:/Users/VN_Ak/AppData/Local/Programs/Python/Python36-32/Lib/site-packages')
from discord.ext import commands
from bs4 import BeautifulSoup
from cogs.utils.utils import Utils as utils

class Nyaa():
    def __init__(self, bot):
        self.bot = bot

    '''
     Return a list of dicts with the results of the query.
    '''
    def search(self, keyword, **kwargs):

        category = kwargs.get('category', 0)
        subcategory = kwargs.get('subcategory', 0)
        filters = kwargs.get('filters', 0)
        page = kwargs.get('page', 0)

        if page > 0:
            r = requests.get("http://nyaa.si/?f={}&c={}_{}&q={}&p={}".format(filters, category, subcategory, keyword, page))
        else:
            r = requests.get("http://nyaa.si/?f={}&c={}_{}&q={}".format(filters, category, subcategory, keyword))

        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.select('table tr')

        results = {}

        if rows:
            results = utils.parse_nyaa(rows, limit=None)

        return results

    def searchsukei(self, keyword, **kwargs):

        category = kwargs.get('category', 0)
        subcategory = kwargs.get('subcategory', 0)
        filters = kwargs.get('filters', 0)
        page = kwargs.get('page', 0)

        if page > 0:
            r = requests.get("http://sukebei.nyaa.si/?f={}&c={}_{}&q={}&p={}".format(filters, category, subcategory, keyword, page))
        else:
            r = requests.get("http://sukebei.nyaa.si/?f={}&c={}_{}&q={}".format(filters, category, subcategory, keyword))

        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.select('table tr')

        results = {}

        if rows:
            results = utils.parse_nyaa_suke(rows, limit=None)

        return results
    
    '''
     Returns an array of dicts with the n last updates of Nyaa.si
    '''
    def news(number_of_results):
        r = requests.get("http://nyaa.si/")
        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.select('table tr')

        return utils.parse_nyaa(rows, limit=number_of_results + 1)

    @commands.command(name="nyaa", pass_context=True)
    async def nyaa(self, ctx, *args):
        """Find torrent on nyaa.si --- [p]nyaa <search>;<how many display>"""
        channel = ctx.message.channel
        userIn = ""
        count = ""
        for count, thing in enumerate(args):
            userIn += '{0}'.format(thing) + " "
        if len(userIn.split(';')) > 1:
            count = userIn.split(';')[1]
        else:
            count = '10';
        result = self.search(userIn)
        if result == 0:
            await self.bot.say("Not found")
        else:
            msg = ""
            if len(result) < int(count):
                count = len(result)
                for res in result[0:int(count):]:
                    msg += "Name: " + res['name'] + "\n" + "Category: " + res['category'] + "\n" + "Url: " + res['url'] + "\n" + "Size: " + res['size'] + " --- " + "Date: " + res['date'] + " --- " + "Seeders: " + res['seeders'] + " --- " + "Leechers" + res['leechers'] + "\n"
                    await self.bot.say(msg)
                    msg = ""
            else:
                for res in result[0:int(count):]:
                    msg += "Name: " + res['name'] + "\n" + "Category: " + res['category'] + "\n" + "Url: " + res['url'] + "\n" + "Size: " + res['size'] + " --- " + "Date: " + res['date'] + " --- " + "Seeders: " + res['seeders'] + " --- " + "Leechers" + res['leechers'] + "\n"
                    await self.bot.say(msg)
                    msg = ""

    @commands.command(name="sukeinyaa", pass_context=True)
    async def sukeinyaa(self, ctx, *args):
        """Find torrent on sukebei.nyaa.si --- [p]sukeinyaa <search>;<how many display>"""
        channel = ctx.message.channel
        userIn = ""
        count = ""
        for count, thing in enumerate(args):
            userIn += '{0}'.format(thing) + " "
        if len(userIn.split(';')) > 1:
            count = userIn.split(';')[1]
        else:
            count = '10';
        result = self.searchsukei(userIn)
        if result == 0:
            await self.bot.say("Not found")
        else:
            msg = ""
            if len(result) < int(count):
                count = len(result)
                for res in result[0:int(count):]:
                    msg += "Name: " + res['name'] + "\n" + "Category: " + res['category'] + "\n" + "Url: " + res['url'] + "\n" + "Size: " + res['size'] + " --- " + "Date: " + res['date'] + " --- " + "Seeders: " + res['seeders'] + " --- " + "Leechers" + res['leechers'] + "\n"
                    await self.bot.say(msg)
                    msg = ""
            else:
                for res in result[0:int(count):]:
                    msg += "Name: " + res['name'] + "\n" + "Category: " + res['category'] + "\n" + "Url: " + res['url'] + "\n" + "Size: " + res['size'] + " --- " + "Date: " + res['date'] + " --- " + "Seeders: " + res['seeders'] + " --- " + "Leechers" + res['leechers'] + "\n"
                    await self.bot.say(msg)
                    msg = ""

def setup(bot):
    bot.add_cog(Nyaa(bot))