# main file for repl.it 

from minesweeper.minesweeper import minesweeper
from genericURCLOptimiser.genericURCLOptimiser import genericURCLoptimiser
from URCLEmulator.URCLEmulator import emulate
import discord
import os
from random import randint
from keep_alive import keep_alive
import asyncio
from bCompiler.bCompiler import bCompiler
from MPU6Transpiler.MPU6Transpiler import MPU6Transpile

client = discord.Client()


@client.event
async def on_ready():
    print("Username: " + str(client.user))


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    elif message.content.startswith("$lol"):
        if str(message.author) == "Mod Punchtree#5817":
            await message.channel.send(":regional_indicator_l::regional_indicator_o::regional_indicator_l:")
        elif randint(1, 20) == 1:
            await message.channel.send("```\nFatal - Token too big:\nyoMamma\n      ^\n```")
        else:
            await message.channel.send(":regional_indicator_l::regional_indicator_o::regional_indicator_l:")

    elif message.content.startswith("$help") and str(message.channel) != "urcl-bot":
        await message.channel.send(":woman_shrugging:")
        return

    elif str(message.channel) == "urcl-polls" and message.content.startswith("$poll"):
        
        channel = message.channel
        pollDescription = ""
        options = []
        text = message.content[6:]
        while text.find("```") != -1:
            text = text[text.find("```") + 4: ]
            subText = text[: text.find("```")]
            text = text[text.find("```") + 3: ]
            if not subText:
                await message.channel.send("FATAL - blank block found in message")
                return
            if not pollDescription:
                pollDescription = subText
            else:
                options.append(subText)

        if (len(options) <= 1) or (not pollDescription):
            await message.channel.send("FATAL - at least 2 options are required as well as a description")
            return
        
        options.append("other (post in #urcl-concerns)")
        
        if len(options) > 26:
            await message.channel.send("FATAL - Too many options, there should be less than 27 options")
            return

        await message.delete()

        reactions = []
        finalText = "@here " + pollDescription
        letters = "abcdefghijklmnopqrstuvwxyz"
        for index, option in enumerate(options):
            letter = letters[index]
            reactions.append(letter)
            finalText += "\n" + letter.upper() + ") " + option
        
        finalText += "\n\nPlease vote only once (that includes alt accounts). This poll ends 24 hours after it has been first posted."

        if len(finalText) > 2000:
            await message.channel.send("FATAL - Poll text is too long to be posted")            
            return
        
        pollMessage = await channel.send(finalText)
        translations = ["\U0001F1E6", "\U0001F1E7", "\U0001F1E8", "\U0001F1E9", "\U0001F1EA", "\U0001F1EB", "\U0001F1EC", "\U0001F1ED", "\U0001F1EE", "\U0001F1EF", "\U0001F1F0", "\U0001F1F1", "\U0001F1F2", "\U0001F1F3", "\U0001F1F4", "\U0001F1F5", "\U0001F1F6", "\U0001F1F7", "\U0001F1F8", "\U0001F1F9", "\U0001F1FA", "\U0001F1FB", "\U0001F1FC", "\U0001F1FD", "\U0001F1FE", "\U0001F1FF"]
        for i in range(len(reactions)):
            await pollMessage.add_reaction(translations[i])

        await asyncio.sleep(24 * 3600)
        
        try:
            pollMessage = await channel.fetch_message(pollMessage.id)
        except:
            return
        
        resultsText = "This poll has now finished, the results are:"
        count69 = []
        for i in reactions:
            count69.append(0)
        for reaction in pollMessage.reactions:
            if str(reaction) in translations:
                count69[translations.index(str(reaction))] = reaction.count - 1
                resultsText += "\n" + str(reactions[translations.index(str(reaction))]).upper() + " - " + str(reaction.count - 1)
        winner = count69.index(max(count69))
        if count69.count(max(count69)) > 1:
            resultsText += "\n\nThis poll ended in a tie"
        else:
            resultsText += "\n\nThe winner is: Option " + reactions[count69.index(max(count69))].upper()
        await pollMessage.reply(resultsText)

        return

    elif str(message.channel) != "urcl-bot":
        return

    elif message.content.startswith("$minesweeper"):
        width = 10
        height = 10
        text = minesweeper(width, height, 20)
        answer = ""
        for i, j in enumerate(text):
            if i % height == 0:
                answer += "\n"
            if j == -1:
                answer += "||\U0001F4A3||"
            elif j == 0:
                answer += "||:zero:||"
            elif j == 1:
                answer += "||:one:||"
            elif j == 2:
                answer += "||:two:||"
            elif j == 3:
                answer += "||:three:||"
            elif j == 4:
                answer += "||:four:||"
            elif j == 5:
                answer += "||:five:||"
            elif j == 6:
                answer += "||:six:||"
            elif j == 7:
                answer += "||:seven:||"
            elif j == 8:
                answer += "||:eight:||"
            else:
                raise Exception("FATAL - Unrecognised symbol in minesweeper: " + j)
        await message.channel.send(answer + "\nThe corners are safe!\nThere are 20 mines total.")
        return

    elif message.content.startswith("$help"):
        await message.channel.send("""```c\nTo emulate URCL code do:\n$URCL\n// URCL code goes here\n\nTo compile B code to optimised URCL do:\n$B [wordLength = 8], [numberOfRegisters = 2]\n// B code goes here\n\nTo compile B code to unoptimised URCL do:\n$BAD [wordLength = 8], [numberOfRegisters = 2]\n// B code goes here\n\nTo optimise URCL code do:\n$optimise\n// URCL code goes here\n\nTo "LOL" do:\n$lol\n```""")
        return

    elif message.content.startswith("$BAD"):
        await message.channel.send("Compiling...")
        try:
            text = bCompiler("$B" + message.content[4:])
        except Exception as x:
            await message.channel.send("ERROR: \n" + str(x))
            return
        f = open("output.txt", "w")
        f.write("\n".join(text))
        f.close()
        await message.channel.send(file=discord.File("output.txt"))
        return

    elif message.content.startswith("$B"):
        await message.channel.send("Compiling...")
        if len(message.content) > 2:
            text = message.content[3: message.content.index("\n")]
            if text.find(" ") != -1:
                text1 = text[:text.find(" ")]
                text2 = text[text.find(" ") + 1:]
            else:
                text1 = text
                text2 = "8"
            if text1.isnumeric():
                BITS = text1
            else:
                BITS = "8"
            text = message.content[message.content.index("\n"):]
        else:
            BITS = "8"
            text = message.content[2:]
        try:
            text = bCompiler(message.content)
        except Exception as x:
            await message.channel.send("ERROR: \n" + str(x))
            return
        
        await message.channel.send("Optimising...")
        try:
            text = ("\n".join(genericURCLoptimiser([i.replace(" ", ",").replace(",", " ", 1).replace(",", ", ") for i in text], int(BITS)))).replace(", ", " ")
        except Exception as x:
            await message.channel.send("ERROR: \n" + str(x))
            return
        f = open("output.txt", "w")
        f.write(text)
        f.close()
        await message.channel.send(file=discord.File("output.txt"))
        return
    
    elif message.content.startswith("$MPU6"):
        await message.channel.send("Translating...")
        text = message.content[5: ]
        text = text.split("\n")
        text = MPU6Transpile(text)
        f = open("output.txt", "w")
        f.write(text)
        f.close()
        await message.channel.send(file=discord.File("output.txt"))
        return

    elif message.content.startswith("$URCL"):
        await message.channel.send("Emulating...")
        text = message.content[5: ]
        text = text.upper()
        while text.find("  ") != -1:
            text = text.replace("  ", " ")
        if text.find(",") != -1:
            await message.channel.send("FATAL - Commas are not allowed, use spaces instead")
            return
        text = text.split("\n")
        for i, j in enumerate(text):
            if (j.find(",") == -1) and (j.find("=") == -1):
                text[i] = (j.replace(" ", ", ")).replace(", ", " ", 1)
        text = "\n".join(text)
        try:
            text = emulate(text, False, False)
        except Exception as x:
            await message.channel.send("ERROR: \n" + str(x))
            return
            
        f = open("output.txt", "w")
        f.write(text)
        f.close()
        await message.channel.send(file=discord.File("output.txt"))
        return
    
    elif message.content.startswith("$optimise") or message.content.startswith("$optimize"):
        if message.content[10 :]:
            if message.content[10].isnumeric():
                BITS = int(message.content[10 : message.content.index("\n")])
            else:
                BITS = 8
        else:
            BITS = 8
        await message.channel.send("Optimising...")
        text = message.content[message.content.find("\n"): ]
        text = text.upper()
        while text.find("  ") != -1:
            text = text.replace("  ", " ")
        if text.find(",") != -1:
            await message.channel.send("FATAL - Commas are not allowed, use spaces instead")
            return
        text = text.split("\n")
        for i, j in enumerate(text):
            if (j.find(",") == -1) and (j.find("=") == -1):
                text[i] = (j.replace(" ", ", ")).replace(", ", " ", 1)
        text = "\n".join(text)
        try:
            text = "\n".join(genericURCLoptimiser(text, BITS))
        except Exception as x:
            await message.channel.send("ERROR: \n" + str(x))
            return
        f = open("output.txt", "w")
        f.write(text)
        f.close()
        await message.channel.send(file=discord.File("output.txt"))
        return

    else:
        return

keep_alive()
client.run(os.getenv("TOKEN"))
