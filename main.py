# main file for repl.it 

import discord
import os
from random import randint
from keep_alive import keep_alive
import asyncio

client = discord.Client()


@client.event
async def on_ready():
    print("Username: " + str(client.user))


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    elif message.content.startswith("$help"):
        await message.channel.send(":woman_shrugging:")
        return

    elif str(message.channel) != "flagless-urcl-bot":
        return
    
    elif message.content.startswith("$URCL"):
        await message.channel.send("Emulating...")
        return

    elif message.content.startswith("$B"):
        await message.channel.send("Compiling...")
        if len(message.content) > 2:
            text = message.content[3:message.content.index("\n")]
            if text.find(" ") != -1:
                text1 = text[:text.find(" ")]
                text2 = text[text.find(" ") + 1:]
            else:
                text1 = text
                text2 = "2"
            if text1.isnumeric():
                BITS = text1
            else:
                BITS = "8"
            text = message.content[message.content.index("\n"):]
        else:
            BITS = "8"
            text = message.content[2:]
        await message.channel.send("```\n" +
                                   compile(text, int(BITS), int(text2)) +
                                   "```")
        return
    
    elif message.content.startswith("$MPU6"):
        await message.channel.send("Translating...")
        text = message.content[5:]
        text = text.split("\n")
        text = MPU6Transpile(text)
        try:
            await message.channel.send("```\n" +
                                   text +
                                   "```")
        except Exception:
            f = open("output.txt", "w")
            f.write(text)
            f.close()
            await message.channel.send("Output too big! ;)")
            await message.channel.send(file=discord.File("output.txt"))
        return
        
    else:
        return

keep_alive()
client.run(os.getenv("TOKEN"))
