import discord
from replit import db
import lobby as l
import asyncio
import sys
import sheet
import matplotlib.pyplot as plt

#################################
## COMMANDES LIEES AUX JOUEURS ##
#################################

async def participate(client: discord.Client, message: discord.Message):
    player = message.author
    embed = discord.Embed(title="Inscription", color=0xf5a816)
    embed.add_field(name=player.name, value=player.id, inline=False)
    if player.id in db:
        embed.add_field(
            name="Statut", value="❌ Utilisateur déjà inscrit", inline=False)
    else:
        db[player.id] = {"ELO": [0], "decks": {}, "W": [], "L": [], "D2P": [*db["decks"]][0], "canID" : 0}
        embed.add_field(
            name="Statut", value="✅ Utilisateur enregistré", inline=False)
    await message.channel.send(embed=embed)


async def leaderboard(client: discord.Client, message: discord.Message):
    keys = db.keys()
    names = []
    value = []
    for key in keys:
      try:
        print(int(key))
        user = await client.fetch_user(int(key))
        if user != None:
            print(user.name)
            names.append(user)
      except:
        print("err: "+key)
    names.sort(key=lambda x: db[str(x.id)]['ELO'][-1], reverse=True)
    description = ""
    for name in names:
      description += "{}: {}\n".format(name.name, db[str(name.id)]['ELO'][-1])

    embed = discord.Embed(title="Leaderboard", description = description, color=0xf5a816)
    await message.channel.send(embed=embed)


async def win(client: discord.Client, message: discord.Message):
  user = message.author
  embed = discord.Embed(title="Close lobby", color=0xf5a816)
  index = l.checkLobby(user.id)
  if index == -1:
    embed.add_field(name="Statut", value=user.name+" ne fait partie d'aucun lobby")
  elif len(db['lobby']["players"][index])<2:
    embed.add_field(name="Statut", value="Vous n'avez pas encore d'adversaire")
  else:
    p1 = await client.fetch_user(int(db['lobby']["players"][index][0]))
    p2 = await client.fetch_user(int(db['lobby']["players"][index][1]))
    if p2 == user:
      p1 = await client.fetch_user(int(db['lobby']["players"][index][1]))
      p2 = await client.fetch_user(int(db['lobby']["players"][index][0]))
    embed.add_field(name=p1.name, value=p1.id, inline=False)
    embed.add_field(name=p2.name, value=p2.id, inline=False)
    embed.add_field(name="Statut", value="Veuillez confirmer la victoire de "+ user.name, inline=False)
  msg = await message.channel.send(embed=embed)
  await msg.add_reaction("✅")
  await msg.add_reaction("❌")

  await asyncio.sleep(60)

  try:
    await msg.delete()
    gain = l.closeLobby(index, p1.id, p2.id)
    embed = discord.Embed(title="Résultat", color=0xf5a816)
    embed.add_field(name=p1.name, value="+ "+str(gain), inline=False)
    embed.add_field(name=p2.name, value="- "+str(gain), inline=False)
    await message.channel.send(embed=embed)
  except:
    print("lobby déjà close")
  
async def stat(client: discord.Client, message:discord.Message):
  #recup tous les messages
  if message.content[1:5] == 'stat':
    keys = db.keys()
    compt = 0
    for key in keys:
      try:
        user = await client.fetch_user(int(key))
        if user.name in message.content:
          ELO = db[str(user.id)]["ELO"]
          plt.plot(ELO, label=user.name)
          await indivStat(client, message, user)
          compt +=1
        if "all" in message.content:
          ELO = db[str(user.id)]["ELO"]
          plt.plot(ELO, label=user.name)
          compt +=1
      except:
        print("err: "+key)
    if compt == 0:
      embed = discord.Embed(title="Close lobby", description="❌ Les noms inscrits ne participent pas à la Gryphon League", color=0xf5a816)
      await message.channel.send(embed=embed)
      return 0
    
    plt.grid(True)
    plt.legend()
    plt.ylabel('ELO')
    plt.xlabel('nombre de parties')
    plt.savefig('graph.png')
    await message.channel.send(file=discord.File('graph.png'))
    plt.clf()
  else:
    await indivStat(client, message, message.author)


async def indivStat(client: discord.Client, message:discord.Message,user: discord.User):
  embed = discord.Embed(title=user.name, color=0xf5a816)

  # AVATAR
  embed.set_thumbnail(url=user.avatar_url)

  # DECK ACTUEL
  embed.add_field(name="Deck", value=db[str(user.id)]["D2P"], inline=False)

  # CURRENT ELO
  embed.add_field(name="ELO", value=db[str(user.id)]["ELO"][-1], inline=False)

  # MAX ELO
  embed.add_field(name="Record", value=max(db[str(user.id)]["ELO"]), inline=False)

  # AVERAGE
  ELO = db[str(user.id)]["ELO"]
  if len(ELO) > 1:
    win = 0
    for i in range(len(ELO)-1):
      if ELO[i]<ELO[i+1]:
        win += 1

    embed.add_field(name="Ratio", value = str(win/(len(ELO)-1) * 100)+" %", inline=False)

  # RATIO PAR DECKS

  stat = ""
  for deck in db[str(user.id)]["decks"].keys():
    w = db[str(user.id)]["decks"][deck]["W"]
    l = db[str(user.id)]["decks"][deck]["L"]
    stat += "{}: {}% ({}-{})\n".format(deck, 100*w/(w+l), w, l)

  embed.add_field(name="Ratio", value = stat, inline=False)

  # NB DE GAMES
  if len(ELO) > 1:  
    embed.add_field(name="Nombre de parties", value = len(ELO)-1, inline=False)


  await message.channel.send(embed=embed)


    
async def winProcess(client: discord.Client, reaction, embeds):
  print("in")
  p1 = embeds[0].to_dict()['fields'][0]['value']
  p2 = embeds[0].to_dict()['fields'][1]['value']
  
  p1 = await client.fetch_user(p1)
  p2 = await client.fetch_user(p2)
  reactions = reaction.message.reactions
  for reac in reactions:
    if reac.emoji == '✅':
      users = await reac.users().flatten()
      if p2 in users:
        print("CHECK CONFIRME")
        #TODO compléter si le score est accepté
        await reaction.message.delete()
        index = l.checkLobby(p1.id)
        gain = l.closeLobby(index, p1.id, p2.id)
        embed = discord.Embed(title="Résultat", color=0xf5a816)
        embed.add_field(name=p1.name, value="+ "+str(gain), inline=False)
        embed.add_field(name=p2.name, value="- "+str(gain), inline=False)
        await reaction.message.channel.send(embed=embed)
        break
        
    if reac.emoji == '❌':
      
      users = await reac.users().flatten()
      for member in users:
        print(member.name)
      for member in users:
        if member == p1 or member == p2:
          #TODO compléter si ile score est refusé
          await reaction.message.delete()
          break
    


