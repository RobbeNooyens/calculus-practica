from random import randint

import discord

import config

client = discord.Client()
exercises: list = []
claimed: list = []
statusmessage = None
CHANNELS = [810946686728929300, 810920527736340550, 541408928408272938]
prefix = "%"
load_str = prefix + "load "
claim_str = prefix + "claim "
unclaim_str = prefix + "unclaim "

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id in CHANNELS:
        if message.content.startswith(load_str):
            exercises.clear()
            claimed.clear()
            data: str = message.content.replace(load_str, "")
            data = data.strip('\n\t ')
            reeksen = data.split('\n')
            for reeks in reeksen:
                components = reeks.split(' / ')
                if len(components) != 2:
                    continue
                name = components[0]
                toread = components[1]
                for ex in toread.split('; '):
                    exercises.append(name+"-"+ex)
            print(exercises)
            await message.delete()
            reply = await message.channel.send(
                "De oefeningen zijn ingelezen! Klik op onderstaande emoji om een oefeningen toegewezen te krijgen of typ " + claim_str + "<oefeningnr>")
            await reply.add_reaction("\N{THUMBS UP SIGN}")
            await message.channel.send("Resterende oefeningen: " + ' | '.join([e for e in exercises]))
        if message.content.startswith(claim_str):
            ex = message.content.replace(claim_str, "").strip()
            if ex not in exercises:
                await message.author.send("Ik begrijp niet welke oefening je bedoelt. Je moet de volledige oefening meegegeven zoals hij in mijn lijst staat.")
            else:
                claimed.append(ex)
                exercises.remove(ex)
                await message.author.send("Je hebt oefening " + ex + " geclaimed. Veel succes!")
                await message.channel.send("Resterende oefeningen: " + ' | '.join([e for e in exercises]))
            await message.delete()
        elif message.content.startswith(unclaim_str):
            ex = message.content.replace(unclaim_str, "").strip()
            if ex in claimed:
                claimed.remove(ex)
                exercises.append(ex)
                await message.channel.send("Resterende oefeningen: " + ' | '.join([e for e in exercises]))
            await message.delete()



@client.event
async def on_reaction_add(reaction, user):
    emoji = reaction.emoji

    if user.bot:
        return

    if emoji == "\N{THUMBS UP SIGN}" and reaction.message.author.bot:
        oefening: str = exercises.pop(randint(0, len(exercises)-1))
        claimed.append(oefening)
        await reaction.message.channel.send("Resterende oefeningen: " + ' | '.join([e for e in exercises]))
        await user.send("Je kan volgende oefening maken: " + oefening)
        await user.send("Veel succes!")

    return


client.run(config.TOKEN)
