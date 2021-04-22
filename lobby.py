import discord 
from replit import db
import functions as fnct 
import asyncio

################################
## FONCTION INTERNE AUX LOBBY ##
################################

def checkLobby(id:int):
  lobbies = db["lobby"]["players"]
  index = 0
  for lob in lobbies:
    if id in lob:
      return index
    index += 1
  return -1

def closeLobby(index:int, p1:int, p2:int):
  gain = fnct.elo(p1, p2)
  lobbies = db["lobby"]
  if len(lobbies["players"]) == 1:
    lobbies["players"] = [[]]
  else:
    del lobbies["players"][index]
  db["lobby"] = lobbies
  return gain 


################################
## COMMANDES LIEES  AUX LOBBY ##
################################

async def can(client: discord.Client, message: discord.Message):
    embed = discord.Embed(title="Lobby", color=0xf5a816)
    lobbies = db["lobby"]

    index = 1
    if checkLobby(message.author.id) > -1:
      embed.add_field(
          name="Statut",
          value="❌ " + message.author.name + " is already in a lobby", 
          inline=False)
      await message.channel.send(embed=embed)
      return 0
    else:
      for lob in lobbies["players"]:
        if message.author.id not in db.keys():
          embed.add_field(
              name="Statut",
              value="❌ " + message.author.name + " is not registered", 
              inline=False)
          await message.channel.send(embed=embed)
          return 0
        elif db[str(message.author.id)]["D2P"] == None:
          embed.add_field(
              name="Statut",
              value="❌ " + message.author.name + " doesn't have a valid deck", 
              inline=False)
          await message.channel.send(embed=embed)
          return 0
        elif len(lob) == 0:
          playerDB = db[str(message.author.id)]
          playerDB["canID"] += 1
          lob.append(message.author.id)
          embed.add_field(
              name="Statut",
              value="✅ " + message.author.name + " joined lobby "+ str(index) + " (1/2)", 
              inline=False)
        elif len(lob) == 1:
          playerDB = db[str(message.author.id)]
          playerDB["canID"] += 1
          lob.append(message.author.id)
          embed.add_field(
              name="Statut",
              value="✅ " + message.author.name + " joined lobby "+ str(index) + " (2/2)",
              inline=False)
        elif index == len(lobbies["players"]):
          lobbies["players"].append([])
        index += 1

    db["lobby"] = lobbies
    db[str(message.author.id)] = playerDB
    
    canID = db[str(message.author.id)]["canID"]

    await message.channel.send(embed=embed)

    await asyncio.sleep(3600)

    if canID == db[str(message.author.id)]["canID"]:
      await drop(client, message)



async def drop(client: discord.Client, message: discord.Message):
  user = message.author
  index = checkLobby(user.id)
  lobbies = db["lobby"]
  embed = discord.Embed(title="Drop lobby", color=0xf5a816)
  if index == -1:
    return -1
  else:
    lobbies["players"][index].remove(user.id)
    embed.add_field(name="Statut", value=user.name+" left lobby "+str(index+1))
    for lob in lobbies["players"]:
      if len(lob) == 1:
        p = lob[0]
        if p not in lobbies["players"][index]:
          lobbies["players"][index].append(p)
          lobbies["players"].pop()
  db["lobby"] = lobbies
  print(db["lobby"])
  await message.channel.send(embed=embed)

async def listOfLobbies(client: discord.Client, message: discord.Message):
  embed = discord.Embed(title="Lobby", color=0xf5a816)
  lobbies = db["lobby"]["players"]
  index = 1
  for lob in lobbies:
    p1 = None
    p1name = " "
    d1name = ""
    p2 = None
    p2name = " "
    d2name = ""
    if len(lob) >= 1:
      p1 = await client.fetch_user(int(lob[0]))
      p1name = p1.name
      d1name = '('+db[str(p1.id)]['D2P']+')'
    if len(lob) == 2:
      p2 = await client.fetch_user(int(lob[1]))
      p2name = p2.name
      d2name = '('+db[str(p2.id)]['D2P']+')'
    
    embed.add_field(
            name="Lobby "+str(index)+" ("+str(len(lob))+"/2)",
            value="{} {} vs {} {}".format(p1name, d1name, p2name, d2name),
            #value=p1 + " ("+ +" vs "+p2,
            inline=False)
    index += 1
  await message.channel.send(embed=embed)


