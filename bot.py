import os
import discord
import config
from datetime import datetime
from discord.ext import commands
from jobs_scraping import scrap_internshala

TOKEN = ''

client = commands.Bot(command_prefix=">")

@client.event
async def on_ready():
    print("Bot is ready!")

@client.command()
async def hello(ctx):
    await ctx.send("hi, sumit!")

@client.command()
async def DataScience(message):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d")

    table = scrap_internshala(config.internshala_data_dict, config.INTERNSHALA_DB)

    for post in table.find({"Date Time": date_time}):
        await message.send("```"+ \
                            "COMPANY       : " + post['company'] + "\n" + \
                            "PROFILE       : " + post['profile'] + "\n" + \
                            "OFFER         : " + post['Offer'] + "\n" + \
                            "START DATE    : " + post['Start Date'] + "\n" + \
                            "APPLY BY DATE : " + post['Apply by Date'] + "\n" + \
                            "DURATION      : " + post['Duration'] + "\n" + \
                            "STIPEND       : " + post['Stipend'] + "\n" \
                           +"```")
        await message.send(post['url'])
        await message.send("`" + "-"*40 + "`")


client.run(TOKEN)