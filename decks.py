import discord 
from replit import db
import matplotlib.pyplot as plt
import numpy as np
import player as pl


async def decks(client: discord.Client, message: discord.Message):
  decks = ""
  for deck in db["decks"].keys():
    decks += (deck+"\n")
  if decks == "":
    decks = "none"

  embed = discord.Embed(title="Decks", description=decks, color=0xf5a816)
  await message.channel.send(embed=embed)

async def addDeck(client: discord.Client, message: discord.Message):

  i = 0
  for char in message.content:
    if char == " ":
      deckName = message.content[i+1:]
      break
    i += 1

  keys = db["decks"].keys()
  dbDecks = db["decks"]
  dbDecks[deckName] = len(keys)

  mat = db["mat"]

  if len(mat)>0 :
    mat.append(([0] * len(keys)))
    mat = [x + [0] for x in mat]
  
  else:
    mat = [[0]]

  print(mat)

  db["mat"] = mat
  db["decks"] = dbDecks
  print(db["decks"])
  await message.channel.send("done")


async def setDeck(client: discord.Client, message: discord.Message):
  user = message.author
  deck = message.content
  i = 0
  for char in deck:
    if char == " ":
      deck = deck[i+1:]
      break
    i += 1
  print(deck)
  player = db[str(user.id)]
  state = ""
  print(db["decks"].keys())
  if deck.lower() in [x.lower() for x in db["decks"].keys()]:
    index = [x.lower() for x in db["decks"].keys()].index(deck.lower())
    print(index)
    player["D2P"] = [*db["decks"]][index]
    state = [*db["decks"]][index]+" is now your default deck"
  else:
    state = deck+" is not a playable deck"
  
  db[str(user.id)] = player
  
  embed = discord.Embed(title=user.name, description=state, color=0xf5a816)
  embed.set_thumbnail(url=user.avatar_url)
  await message.channel.send(embed=embed)

async def plotDecks(client: discord.Client, message: discord.Message):
  fig, ax = plt.subplots()
  mat = np.array(db["mat"])
  size = len(db["decks"].keys())
  plt.xticks(np.arange(size), db["decks"].keys(),rotation=90)
  plt.yticks(np.arange(size), db["decks"].keys())


  ax.matshow(mat, cmap=plt.cm.RdYlGn)

  for i in range(size):
      for j in range(size):
          c = mat[j,i]
          ax.text(i, j, str(c), va='center', ha='center')

  plt.savefig('graph.png')
  await message.channel.send(file=discord.File('graph.png'))
  plt.clf()