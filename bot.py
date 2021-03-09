from random import randint

import discord

import config

client = discord.Client()
exercises: list = []
claimed: dict = {}
statusmessage = None
CHANNELS = [810946686728929300, 810920527736340550, 541408928408272938]
prefix = "%"
load_str = prefix + "load "
claim_str = prefix + "claim "
unclaim_str = prefix + "unclaim "
done_str = prefix + "done "
overview_str = prefix + "overview"

permits = [238005886738628608, 434749785518505984]

def permissible(author):
    for uuid in permits:
        if author.id == uuid:
            return True
    return False


@client.event
async def on_message(message):
    if message.author.bot or not message.content.startswith(prefix):
        return
    if message.channel.id in CHANNELS:
        if message.author.id not in claimed.keys():
            claimed[message.author.id] = list()

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
                    exercises.append(name + "-" + ex)
            print("[LOAD]\t Gebruiker", message.author.display_name, '(', str(message.author.id), ') heeft oefeningen ingeladen:', exercises)
            await message.delete()
            reply = await message.channel.send(
                "De oefeningen zijn ingelezen! Klik op onderstaande emoji om een oefeningen toegewezen te krijgen of typ " + claim_str + "<oefeningnr>")
            await reply.add_reaction("\N{THUMBS UP SIGN}")
            await message.channel.send("Resterende oefeningen: " + ' | '.join([e for e in exercises]))
        elif message.content.startswith(claim_str):
            ex = message.content.replace(claim_str, "").strip()
            if ex not in exercises:
                await message.author.send(
                    "Ik begrijp niet welke oefening je bedoelt. Je moet de volledige oefening meegegeven zoals hij in mijn lijst staat.")
            else:
                claimed[message.author.id].append(ex)
                exercises.remove(ex)
                print("[CLAIM]\t Gebruiker", message.author.display_name, '(', str(message.author.id), ') heeft oefening',
                      ex, 'geclaimd.')
                await message.author.send("Je hebt oefening " + ex + " geclaimed. Veel succes!")
                await message.channel.send("Resterende oefeningen: " + ' | '.join([e for e in exercises]))
            await message.delete()
        elif message.content.startswith(unclaim_str):
            ex = message.content.replace(unclaim_str, "").strip()
            if ex in claimed[message.author.id]:
                claimed[message.author.id].remove(ex)
                exercises.append(ex)
                print("[UNCLAIM]\t Gebruiker", message.author.display_name, '(', str(message.author.id),
                      ') heeft oefening',
                      ex, 'vrijgegeven.')
                await message.channel.send("Resterende oefeningen: " + ' | '.join([e for e in exercises]))
            await message.delete()
        elif message.content.startswith(done_str):
            ex = message.content.replace(done_str, "").strip()
            if ex in claimed[message.author.id]:
                claimed[message.author.id].remove(ex)
                print("[DONE]\t Gebruiker", message.author.display_name, '(', str(message.author.id),
                      ') is klaar met oefening ', ex, '.')
                await message.author.send("Ok! Ik heb " + ex + " als afgewerkt aangeduid.")
            await message.delete()
        elif message.content.startswith(overview_str):
            print("[OVERVIEW]\t Gebruiker", message.author.display_name, '(', str(message.author.id),
                  ') heeft een overzicht gegenereerd.')
            build = "Hier is een overzicht van wie aan welke oefening(en) bezig is: \n"
            for uuid in claimed.keys():
                if len(claimed[uuid]) > 0:
                    build += "<@" + str(uuid) + "> : "
                    for ex in claimed[uuid]:
                        build += ex + ", "
                    build = build[:-2]
                    build += '\n'
            await message.channel.send(build)
            await message.delete()
        elif message.content.startswith(prefix + 'filter ') and permissible(message.author):
            exs = message.content.replace(prefix + 'filter ', "").strip().split('; ')
            print("[FILTER]\t Gebruiker", message.author.display_name, '(', str(message.author.id),
                  ') heeft de geclaimde oefeningen gefilterd op: ' + str(exs))
            reply = "De volgende oefeningen zijn door " + message.author.mention + " als afgewerkt gemarkeerd: "
            for uid in claimed:
                for ex in claimed[uid]:
                    if ex not in exs:
                        reply += ex + ', '
                        claimed[uid].remove(ex)
            await message.channel.send(reply[:-2])
            await message.delete()

        elif message.content.startswith(prefix + 'dump') and permissible(message.author):
            print('=' * 30)
            print('\t|', "Memory dump op aanvraag van ", message.author.display_name, '(', str(message.author.id), ')')
            print('\t|', "(List) Exercises:", exercises)
            print('\t|', "(Dict) Claimed:", claimed)
            print('=' * 30)
            await message.add_reaction('\N{THUMBS UP SIGN}')


@client.event
async def on_reaction_add(reaction, user):
    emoji = reaction.emoji

    if user.bot:
        return

    if emoji == "\N{THUMBS UP SIGN}" and reaction.message.author.bot:
        if user.id not in claimed.keys():
            claimed[user.id] = list()
        oefening: str = exercises.pop(randint(0, len(exercises) - 1))
        claimed[user.id].append(oefening)
        print("[RCLAIM]\t Gebruiker", user.display_name, '(', str(user.id), ') heeft oefening', oefening, 'geclaimd.')
        await reaction.message.channel.send("Resterende oefeningen: " + ' | '.join([e for e in exercises]))
        await user.send("Je kan volgende oefening maken: " + oefening)
        await user.send("Veel succes!")

    return


client.run(config.TOKEN)
