import json
import discord
from discord.ext import commands

# TODO implement bot creating rooms that contain 7-14 servers
# TODO implement language private rooms
# TODO implement anon webhooks

bot = commands.Bot(command_prefix="-", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is running")

@bot.event
async def on_message(msg: discord.Message):

    if msg.author.bot:
        return 

    with open("data/all_chat.json","r") as f:
        channels = json.load(f)

        with open("data/codes.json","r") as r:
            codes = json.load(r)

            if msg.channel.id in channels:

                if str(msg.author.id) in codes.keys():

                    code = codes[str(msg.author.id)]

                    for channel in channels:

                        ch = bot.get_channel(channel)
                        
                        if ch != msg.channel:
                            await ch.send(f"Anon#{code}: {msg.content}")

                else: 
                    await msg.reply("Only users on this server can see your messages.")            
                    await msg.channel.send("Use `-join` to join anon chat!")


    await bot.process_commands(msg)

@bot.command()
async def set_channel(ctx: commands.Context, channel: discord.channel.TextChannel):
    
    with open("data/all_chat.json","r") as f:
        channels = json.load(f)

    channels.append(channel.id)
    await ctx.channel.edit(slowmode_delay=5)

    with open("data/all_chat.json","w") as f:
        json.dump(channels, f)

    await ctx.send("Channel added to anon chat!")

@bot.command()
async def join(ctx: commands.Context):

    with open("data/codes.json") as f:
        codes = json.load(f)

    if str(ctx.author.id) in codes:
        await ctx.send("You are already logged!")
        return

    codes[str(ctx.author.id)] = codes["current"]
    codes["current"] += 1

    with open("data/codes.json","w") as f:
        json.dump(codes, f)

    await ctx.send("You are logged to anon chat!")

bot.run("TOKEN")
