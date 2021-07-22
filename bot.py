import json
import os
import random
import time
import urllib.request
from collections import OrderedDict

import discord
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from riotwatcher import LolWatcher

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
lol_watcher = LolWatcher(os.getenv('RIOT_TOKEN'))
my_region = os.getenv('REGION')

client = discord.Client()

@client.event #Message print to console saying that the bot is ready.
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print('--------------------')

@client.event
async def on_member_join(member):
    guild = client.get_guild(833127705054674965)
    await member.channel.send(f'Welcome to the server {member.name}!')


@client.event
async def on_message(message):

    value = random.randint(1,10)

    if message.author == client.user: # If the message sent is from the Bot itself, do nothing
        return

    if value == 1:
        await message.channel.send("Shut up")

    #TODO Help command
    if message.content == '!help':
        return

    if message.content == '!bryant':
        await message.channel.send("No I don't want to go out")

    if message.content == '!joke':
        jokes = json.loads(requests.get(r"https://official-joke-api.appspot.com/random_joke").text)
        print(jokes)
        await message.channel.send(jokes["setup"])
        time.sleep(3)
        await message.channel.send(jokes["punchline"])

    if message.content == '!covid':
        data = json.loads(requests.get(r"https://api.covidtracking.com/v1/us/daily.json").text)
        await message.channel.send(data[0]["death"])

    if message.content == '!cokeTime':
        await message.channel.send(file=discord.File("lib/cokeTime.gif"))

    if message.content == '!embedExample':
        embed=discord.Embed(
        title="Text Formatting",
            url="https://realdrewdata.medium.com/",
            description="Here are some ways to format text",
            color=discord.Color.blue())
        embed.set_author(name="RealDrewData", url="https://twitter.com/RealDrewData", icon_url="https://cdn-images-1.medium.com/fit/c/32/32/1*QVYjh50XJuOLQBeH_RZoGw.jpeg")
        #embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")
        embed.add_field(name="*Italics*", value="Surround your text in asterisks (\*)", inline=False)
        embed.add_field(name="**Bold**", value="Surround your text in double asterisks (\*\*)", inline=False)
        embed.add_field(name="__Underline__", value="Surround your text in double underscores (\_\_)", inline=False)
        embed.add_field(name="~~Strikethrough~~", value="Surround your text in double tildes (\~\~)", inline=False)
        embed.add_field(name="`Code Chunks`", value="Surround your text in backticks (\`)", inline=False)
        embed.add_field(name="Blockquotes", value="> Start your text with a greater than symbol (\>)", inline=False)
        embed.add_field(name="Secrets", value="||Surround your text with double pipes (\|\|)||", inline=False)
        embed.set_footer(text="Learn more here: realdrewdata.medium.com")

        await message.channel.send(embed=embed)

    # Upon calling command send a Embed class that contains DaBaby
    if message.content == '!daBaby':
        file = discord.File("lib/daBaby.png", filename="daBaby.png")
        embed = discord.Embed(
            title="You have summoned DABABY",
            decription="lets goooo",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url="attachment://daBaby.png")
        await message.channel.send(file=file, embed=embed)

    #TODO Send a picture of the league champion and then list all of the base stats in a message
    #using discord embed
    if message.content.startswith('!leaguestats'):
        message_string = message.content.split(" ")
        try:
            print("MESSAGE_STRING[1]" + message_string[1])
            base_stat = message_string[1]
            data_list = get_champ_data_list()
            champ = best_champ_for_stat(base_stat)
            print(champ)
            pic_of_champ = get_champ_portrait(champ)

            descirption_message = "This is the strongest champion for the basestat: " + base_stat
            embed_message = discord.Embed(
                title = champ,
                description=descirption_message,
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=pic_of_champ)
            embed.set_image(url=pic_of_champ)
            await message.channel.send(embed=embed_message)

        except IndexError:
            await message.channel.send("Uh oh! I need a stat to look up! Example Usage: '!leaguestats hp'")
    
    if message.content.startswith("!build"):
        message_string = message.content.split(" ")
        try:
            print("The champ being queried: " + message_string[1])
            champ = message_string[1]
            build = get_pro_builds(champ)

            pic_of_champ = get_champ_portrait(champ)     
            descirption_message = "This is the most recent probuild for the champion: " + champ
            embed = discord.Embed(
                title = champ,
                description = descirption_message,
                color = discord.Color.blurple
            )
            embed.set_thumbnail(url=pic_of_champ)
            embed.set_image(url=pic_of_champ)

        except IndexError:
            await message.channel.send("Uh oh! I need a stat to look up! Example Usage: '!build Aatrox'")


def get_champ_data_list():
    versions = lol_watcher.data_dragon.versions_for_region(my_region)
    champions_version = versions['n']['champion']
    current_champ_list = lol_watcher.data_dragon.champions(champions_version)
    champion_data_list = OrderedDict(current_champ_list['data'])
    return champion_data_list

def best_champ_for_stat(base_stat):
    try:
        data_list = get_champ_data_list()
        sorted_list = OrderedDict()
        for champ in data_list:
            print(data_list[champ]['stats'])
            sorted_list[champ] = data_list[champ]['stats'][base_stat]
        sorted_list = sorted(sorted_list.items(), key = lambda x: int(x[1]), reverse=True)
        return sorted_list[0]
    except KeyError:
        return 1

#use website crawling to grab the league of legends champion portraits!
def get_champ_portrait(champion):
    lol_website_url = "https://na.leagueoflegends.com"
    request = lol_website_url + "/en-us/champions/"+champion #creates the request link
    r = requests.get(request)
    if r.ok: #if the response code is fine
        bs = BeautifulSoup(r.text, 'html.parser') #parse the webpage
        for line in bs.findAll('img'): #look at all the img tags
            original_link = line
            image_link = str(line).lower()
            if "splash" in image_link and str(champion) in image_link and "_0" in image_link: #check to see if the link contains splash art of champion and is the base skin
                return original_link['src'] #grab the link to download? now what do i want to do
    else:
        print("Failed grabbing {}".format(request))
    return None

def main():
    client.run(TOKEN)

if __name__ == "__main__":
    main()
