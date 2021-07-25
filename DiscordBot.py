#created by Grayson LaFleur

import discord, TwitterBot, traceback, json
from discord.ext import tasks

client = discord.Client()

twitterbot = TwitterBot.TwitterAPI()
twitterbot.start_stream_listener()

channel = client.get_channel(0)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    background_task.start()

@client.event
async def on_message(message):
    if message.content.startswith('/setchannel') and message.author != client.user:
        global channel
        channel = message.channel
        await channel.send('This channel is set to the default channel!')
    
    if message.content.startswith('/follow') and not message.content.startswith('/following'):
        if channel is not None:
            splitMessage = message.content.split(" ")
            if len(splitMessage) == 2:
                try:
                    twitterbot.add_follower(splitMessage[1])
                    await channel.send(f'{splitMessage[1]} has been added to your follower list!\nhttps://twitter.com/{splitMessage[1]}')
                except Exception as e:
                    traceback.print_exc()
                    await channel.send(e)
            else:
                await channel.send("Incorrect input. Must look like '/follow *handle*', there cannot be any spaces")
        else:
            await message.channel.send('Please set channel first with /setchannel')

    if message.content.startswith('/unfollow'):
        if channel is not None:
            splitMessage = message.content.split(" ")
            if len(splitMessage) == 2:
                try:
                    twitterbot.remove_follower(splitMessage[1])
                    await channel.send(f'{splitMessage[1]} has been removed from your follower list!\nhttps://twitter.com/{splitMessage[1]}')
                except Exception as e:
                    await message.channel.send(e)
            else:
                await channel.send("Incorrect input. Must look like '/follow *handle*', there cannot be any spaces")
        else:
            await message.channel.send('Please set channel first with /setchannel')

    if message.content.startswith('/following'):
        if channel is not None:
            try:
                users = twitterbot.follower_list()
                accounts = 'Current follower list:\n'
                counter = 1
                for user in users:
                    accounts+=(f'{counter}. | {user}\n')
                    counter += 1
                await channel.send(accounts)
            except Exception as e:
                await channel.send(e)
        else:
            await message.channel.send('Please set channel first with /setchannel')

    if message.content.startswith('/commands'):
        if channel is not None:
            await message.channel.send("/setchannel - sets the channel for the bot to send messages in\n\
/follow *handle* - follows the twitter handle you enter\n\
/unfollow *handle* - unfollows the twitter handle you enter\n\
/following - creates a list of everyone you are currently following")
        else:
            await message.channel.send('Please set channel first with /setchannel')

@tasks.loop(seconds = 5)
async def background_task():
    if channel is not None:
        try:
            print(twitterbot.follower_list())
            if(twitterbot.get_urls()!=None):
                links = []
                links.extend(twitterbot.get_urls())
                twitterbot.clear_links()
                if len(links) > 0:
                    for link in links:
                        await channel.send(link)
        except Exception:
            print('following no one')

f = open('C:\\Users\\vidrinen\Desktop\\API keys\\discordAPI.json')

data = json.load(f)

client.run(data.get("token"))