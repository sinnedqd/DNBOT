import json
import os
import random
import time
import urllib.request
from collections import OrderedDict

import discord
import requests
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
        await message.channel.send(file=discord.File("cokeTime.gif"))

    #TODO Send a picture of the league champion and then list all of the base stats in a message
    #using discord embed
    if message.content.startswith('!leaguestats'):
        message_string = message.content.split(" ")
        try:
            champion = message_string[1]
            data_list = get_champ_data_list()
            await message.channel.send(champion)
            await message.channel.send(data_list[champion]['stats'])
        except IndexError:
            await message.channel.send("Uh oh! I need a stat to look up! Usage: '!leaguestats hp'")
            """
            
            sorted_list = OrderedDict()
            for champ in data_list:
                await message.channel.send(base_stat)
                await message.channel.send(" : ")
                await message.channel.send(data_list[base_stat])
                sorted_list[champ] = data_list[champ]['stats'][base_stat]
            sorted_list = sorted(sorted_list.items(), key = lambda x: int(x[1]), reverse=True)
            #await message.channel.send(sorted_list[champ])
        except IndexError:
            await message.channel.send("Uh oh! I need a stat to look up! Usage: '!leaguestats hp'")
            """


def get_champ_data_list():
    versions = lol_watcher.data_dragon.versions_for_region(my_region)
    champions_version = versions['n']['champion']
    current_champ_list = lol_watcher.data_dragon.champions(champions_version)
    champion_data_list = OrderedDict(current_champ_list['data'])
    return champion_data_list

def get_champ_portraits():
    #coding:utf8    
    cur_path = os.path.abspath(os.curdir)
    
    champion = "https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js"
    championobj =  json.loads(requests.get(champion).text)
    heroIds = championobj['hero']
    # print(championobj)
    # # print(jsonobj)
    for c in heroIds:
        print(c["heroId"])
        url="https://game.gtimg.cn/images/lol/act/img/js/hero/"+str(c["heroId"])+".js"
        # Send request, get response result
        response = requests.get(url)
        text = response.text
    
            # Print the response content of this request
        # print(text)
    
    # Convert response content into Json object
        jsonobj = json.loads(text)
        # print(jsonobj)
            #Get hero name as folder name
        heroname =  jsonobj["hero"]["name"] 
        print(heroname) 
        isExists=os.path.exists(cur_path+'/all skin pictures/'+heroname)
        skinpath =cur_path+'/all skin pictures/'+heroname
        if not isExists:
                    os.makedirs(cur_path+'/all skin pictures/'+heroname)
        # print(heroname)
            #Get all skins
        heroskins = jsonobj["skins"]
        # print(heroskins)
        for s in heroskins:
            skinname = str(s["name"]).replace('','-').replace('/','') #skin name
            skinimage = str(s["mainImg"]) #Skin image path
            if(len(skinimage)!=0): 
                file_suffix = os.path.splitext(skinimage)[1]
                filename = '{}{}{}{}'.format(skinpath,os.sep,skinname,file_suffix)
                urllib.request.urlretrieve(skinimage,filename)
            # print(skinimage)

def main():
    client.run(TOKEN)

if __name__ == "__main__":
    main()
