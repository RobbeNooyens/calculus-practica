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
        if message.content.startswith("%load "):
            exercises.clear()
            data: str = message.content.replace("%load ", "")
            exercises = data.split("; ")
            print(exercises)
            await message.delete()
            reply = await message.channel.send(
                "De oefeningen zijn ingelezen! Klik op onderstaande emoji om een oefeningen toegewezen te krijgen of typ '%claim <oefeningnr>'.")
            await reply.add_reaction("\N{THUMBS UP SIGN}")
            await message.channel.send("Resterende oefeningen: " + ' | '.join([e for e in exercises]))
        if message.content.startswith("%claim "):
            ex = message.content.replace("%claim ", "")
            if not ex in exercises:
                await message.author.send("Deze oefeningen is niet beschikbaar!")
            else:
                exercises.remove(ex)
                await message.author.send("Je hebt oefening " + ex + " geclaimed. Veel succes!")
                await message.channel.send("Resterende oefeningen: " + ' | '.join([e for e in exercises]))
            await message.delete()


@client.event
async def on_reaction_add(reaction, user):
    emoji = reaction.emoji

    if user.bot:
        return

    if emoji == "\N{THUMBS UP SIGN}":
        oefening: str = exercises.pop(0)
        await reaction.message.channel.send("Resterende oefeningen: " + ' | '.join([e for e in exercises]))
        await user.send("Je kan volgende oefening maken: " + oefening)
        await user.send("Veel succes!")

    return


client.run(config.TOKEN)
