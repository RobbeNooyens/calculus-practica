import discord
from random import shuffle
import string

import config

client = discord.Client()
exercises: list = []
statusmessage = None
CHANNELS = [810946686728929300, 810920527736340550, 541408928408272938]


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id in CHANNELS:
        if "load " in message.content:
            exercises.clear()
            data: string = message.content.replace("load ", "")
            try:
                for s in [float(s) for s in data.split("; ")]:
                    exercises.append(s)
            except:
                return
            # shuffle(exercises)
            print(exercises)
            await message.delete()
            reply = await message.channel.send(
                "De oefeningen zijn ingelezen! Klik op onderstaande emoji om een oefeningen toegewezen te krijgen of typ '%claim <oefeningnr>'.")
            await reply.add_reaction("\N{THUMBS UP SIGN}")
            await message.channel.send("Resterende oefeningen: " + ' | '.join([str(e) for e in exercises]))
        if "claim" in message.content and "%" == message.content[0]:
            try:
                nr = float(message.content.replace("claim ", "").replace("=", ""))
            except:
                await message.author.send(message.content.replace("claim ", "") + " is geen geldig nummer!")
                await message.delete()
                return
            if not nr in exercises:
                await message.author.send("Deze oefeningen is al door iemand anders geclaimed!")
            else:
                exercises.remove(nr)
                await message.author.send("Je hebt oefening " + str(nr) + " geclaimed. Veel succes!")
                await message.channel.send("Resterende oefeningen: " + ' | '.join([str(e) for e in exercises]))
            await message.delete()


@client.event
async def on_reaction_add(reaction, user):
    emoji = reaction.emoji

    if user.bot:
        return

    if emoji == "\N{THUMBS UP SIGN}":
        oefening: float = exercises.pop(0)
        await reaction.message.channel.send("Resterende oefeningen: " + ' | '.join([str(e) for e in exercises]))
        await user.send("Je kan volgende oefening maken: " + str(oefening))
        await user.send("Veel succes!")

    return


client.run(config.TOKEN)
