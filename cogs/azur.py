import asyncio
import re
import requests
import aiohttp
import json
import discord
import os
import glob
import io
import sys
sys.path.append('C:/Users/VN_Ak/AppData/Local/Programs/Python/Python36-32/Lib/site-packages')
from discord.ext import commands
from cogs.utils.checks import *
import bs4
from bs4 import BeautifulSoup
from urllib import parse
from urllib.request import Request, urlopen
import math
from math import sqrt
from cogs.utils.dataIO import dataIO

class azur:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['shipStat'])
    async def shipstat(self, ctx, *, txt: str=None):
        """Find ship status. Ex: [p]shipstat <ship name>"""
        if not txt:
            return await self.bot.say('Input a ship name to check ship stat. Ex: ```\n<p>shipstat akagi```')
        shipListUrl = "https://azurlane.koumakan.jp/List_of_Ships"
        shipListPage = requests.get(shipListUrl)
        shipListSoup = BeautifulSoup(shipListPage.content, "html.parser")
        if(shipListSoup.find("a", {"title":txt.title()})):
            name = txt.title()
            shipName= ""
            checkTxt = name.split()
            if len(checkTxt) > 1:
                shipName = '_'.join(checkTxt)
            else:
                shipName = name
            #base variable
            baseAddress = 'https://azurlane.koumakan.jp/'
            baseAddressImg = 'https://azurlane.koumakan.jp'
            req = baseAddress + shipName
            webpage = requests.get(req)
            soup = BeautifulSoup(webpage.content, "html.parser")
            pretty_soup = soup.prettify()
            imgs = soup.find_all("img")
            iconTxt = txt.title() + "Icon.png"
            iconUrl = baseAddressImg + ""
            tables = soup.find_all("table")
            ths = soup.find_all("th")
            tds = soup.find_all("td")
            data = []
            #Get ship info
            for tbody in tables:
                data.append(tbody.text)
            shipInfo = data[0].splitlines()
            shipInfo = list(filter(None, shipInfo))
            em = discord.Embed(color=0xaa550f,title = shipInfo[0], description='\n**Status:**', url=req)
            #Get icon image
            for img in imgs:
        	    if iconTxt in img.get("alt"):
        		    iconUrl += img.get("src")
            try:
                em.set_thumbnail(url = iconUrl)
            except:
                pass
            #Get stat ship and append to string
            statData = {}
            #Loop get stat character
            for tag in ths:
                if tag.find("img", {"title": "Firepower"}) != None:
                    statData.update({"Firepower":tag.text.rstrip()})
                if tag.find("img", {"title": "Health"}) != None:
                    statData.update({"Health":tag.text.rstrip()})
                if tag.find("img", {"title": "Anti-Air"}) != None:
                    statData.update({"Anti-Air":tag.text.rstrip()})
                if tag.find("img", {"title": "Evasion"}) != None:
                    statData.update({"Evasion":tag.text.rstrip()})
                if tag.find("img", {"title": "Aviation"}) != None:
                    statData.update({"Aviation":tag.text.rstrip()})
                if tag.find("img", {"title": "Torpedo"}) != None:
                    statData.update({"Torpedo":tag.text.rstrip()})

            
            #Loop get stat number and join stat
            statDataNum = {}
            for tag in tds:
                if tag.find("img", {"title": "Firepower"}) != None:
                    if "→" in tag.text:
                        statDataNum.update({"Firepower:": statData["Firepower"] + tag.text})
                if tag.find("img", {"title": "Health"}) != None:
                    if "→" in tag.text:
                        statDataNum.update({"Health:":statData["Health"] + tag.text})
                if tag.find("img", {"title": "Anti-Air"}) != None:
                    if "→" in tag.text:
                        statDataNum.update({"Anti-Air:":statData["Anti-Air"] + tag.text})
                if tag.find("img", {"title": "Evasion"}) != None:
                    if "→" in tag.text:
                        statDataNum.update({"Evasion:":statData["Evasion"] + tag.text})
                if tag.find("img", {"title": "Aviation"}) != None:
                    if "→" in tag.text:
                        statDataNum.update({"Aviation:":statData["Aviation"] + tag.text})
                if tag.find("img", {"title": "Torpedo"}) != None:
                    if "→" in tag.text:
                        statDataNum.update({"Torpedo:":statData["Torpedo"]+ tag.text})

            for tag in tds:
                if tag.find("img", {"alt": "Armor.png"}) != None:
                    if "Light\n" in tag.text or "Medium\n" in tag.text or "Heavy\n" in tag.text:
                        statDataNum.update({"Armor:":tag.text})
                if tag.find("img", {"title": "Reload"}) != None:
                    if "→" in tag.text:
                        statDataNum.update({"Reload:":tag.text})
                if tag.find("img", {"alt": "Consumption.png"}) != None:
                    if "→" in tag.text:
                        statDataNum.update({"Consumption:":tag.text})

            statString = ""
            for dataNum in statDataNum:
                statString += dataNum + statDataNum[dataNum]
            #Get drop location
            drop = soup.find_all('td', {"rowspan": "3"})
            dropLoc = ""
            for item in drop:
                if item.text != "\n":
                    dropLoc += item.text

            #Lb and Skill
            trs = soup.find_all('tr')
            lbList = []
            for tag in trs:
                if "First" in tag.text:
                    lbList.append(tag.text)
                if "Second" in tag.text:
                    lbList.append(tag.text)
                if "Third" in tag.text:
                    lbList.append(tag.text)
            first = list(filter(None, lbList[0].splitlines()))
            second = list(filter(None, lbList[1].splitlines()))
            third = list(filter(None, lbList[2].splitlines()))

            lbDict = {}
            for index, item in enumerate(first, start=0):
                if index % 2 == 0:
                    lbDict.update({"**"+item+"**"+": ":"holder"+"\n"})
                else:
                    lbDict.update({"**"+first[index - 1]+"**"+": ":item+"\n"})
            for index, item in enumerate(second, start=0):
                if index % 2 == 0:
                    lbDict.update({"**"+item+"**"+": ":"holder"+"\n"})
                else:
                    lbDict.update({"**"+second[index - 1]+"**"+": ":item+"\n"})
            for index, item in enumerate(third, start=0):
                if index % 2 == 0:
                    lbDict.update({"**"+item+"**"+": ":"holder"+"\n"})
                else:
                    lbDict.update({"**"+third[index - 1]+"**"+": ":item+"\n"})

            lbDict = dict((k, v) for k, v in lbDict.items() if v != "holder\n")
            lbString = ""
            skillString = ""
            x = list(lbDict.keys())
            for lb in range(len(x)):
                if lb % 2 == 0:
                    if "--" not in lbDict[x[lb]]:
                        lbString += x[lb] + lbDict[x[lb]]
                else:
                    if "--" not in lbDict[x[lb]]:
                        skillString += x[lb] + lbDict[x[lb]]
            #GetImage
            imageTxt = txt.title() + ".png"
            imageUrl = baseAddressImg + ""
            for img in imgs:
                if imageTxt in img.get("alt"):
                    imageUrl += img.get("src")
            #Add Embed
            em.add_field(name=shipInfo[1], value=shipInfo[2])
            em.add_field(name=shipInfo[3],value=shipInfo[4])
            em.add_field(name=shipInfo[5], value=shipInfo[6])
            em.add_field(name=shipInfo[7],value=shipInfo[8])
            em.add_field(name=shipInfo[9], value=shipInfo[10])
            em.add_field(name=shipInfo[11],value=shipInfo[12])
            em.add_field(name="Ship Stat", value=statString)
            em.add_field(name="Drop Location", value=dropLoc)
            em.add_field(name="Limit Break Ranks", value=lbString)
            em.add_field(name="Skills", value=skillString)
            try:
                em.set_image(url = imageUrl)
            except:
                pass
            await self.bot.say(content = None, embed = em)
        else:
            await self.bot.say("There is no ship name: " + txt.title())

def setup(bot):
    bot.add_cog(azur(bot))

