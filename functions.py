import discord 
from replit import db
import numpy as np
import sheet

def updateMat(deckWin: str, deckLoose: str):
  mat = db["mat"]
  mat[db["decks"][deckWin]][db["decks"][deckLoose]] += 1
  db["mat"] = mat

def elo(p1: int, p2: int, manuelMode:bool = False):
  print("IN ELO")

  #acces aux db
  p1db = db[str(p1)]
  p2db = db[str(p2)]

  #ELO
  print(p1db["ELO"][-1], p2db["ELO"][-1])
  gain = int((1+30*(1/(1+10**((p1db["ELO"][-1]-p2db["ELO"][-1])/4000))))*10)
  print(gain)
  p1db["ELO"].append(p1db["ELO"][-1]+gain)
  p2db["ELO"].append(max(0, p2db["ELO"][-1]-gain))

  #Decks stat joueurs
  p1decks = p1db["decks"].keys()
  print(p1decks)
  if p1db["D2P"] in p1decks:
    p1db["decks"][p1db["D2P"]]["W"] += 1
  else:
    p1db["decks"][p1db["D2P"]] = {}
    p1db["decks"][p1db["D2P"]]["W"] = 1
    p1db["decks"][p1db["D2P"]]["L"] = 0

  p2decks = p2db["decks"].keys()
  if p2db["D2P"] in p2decks:
    p2db["decks"][p2db["D2P"]]["L"] += 1
  else:
    p2db["decks"][p2db["D2P"]] = {}
    p2db["decks"][p2db["D2P"]]["W"] = 0
    p2db["decks"][p2db["D2P"]]["L"] = 1
  
  updateMat(p1db["D2P"], p2db["D2P"])

  db[str(p1)] = p1db
  db[str(p2)] = p2db
  print(gain)

  sheet.updateDatas()

  return gain

async def saveDataBase(client: discord.Client, message: discord.Message):
  print("in")
  keys = db.keys()
  dbS0 = {}
  for key in keys:
    #del db[key]
    if key != "s0":
      dbS0[key] = db[key] 
      
  db["s1"]=dbS0
  print(db["s1"])
  await message.channel.send("done")

async def setDataBase(client: discord.Client, message: discord.Message):
  dbS0 = db["s0"]
  dbDecks = db["decks"]
  for key in db.keys():
    del db[key]

  for key in dbS0.keys():
    db[key] = dbS0[key]
  
  db["lobby"] = {"players":[[]],"close":[[]]}
  db["decks"] = {}
  db["mat"] = []
  db["s0"] = dbS0

  await message.channel.send("done")

async def manualMatch(client: discord.Client, message: discord.Message):
  space = []
  index = 0
  for c in message.content:
    if c == ' ':
      space.append(index)
    index += 1
  space.append(len(message.content))

  p1name = message.content[space[0]+1:space[1]]
  p1name = p1name.replace("*"," ")
  p2name = message.content[space[1]+1:space[2]]
  p2name = p2name.replace("*"," ")
  d1name = message.content[space[2]+1:space[3]]
  d2name = message.content[space[3]+1:space[4]]

  print(p1name, p2name)

  #JUST FOR DECKS

  if p1name == "." and p2name == ".":
    updateMat(d1name, d2name)
    await message.channel.send("done")
    return


  #JOUEURS
  p1 = None
  p2 = None
  keys = db.keys()
  for key in keys:
    try:
      user = await client.fetch_user(int(key))
      if user.name in p1name:
        print("find p1")
        p1 = user
      elif user.name in p2name:
        print("find p2")
        p2 = user
    except:
      print("err: "+key)
    
  if p1 is None or p2 is None:
    print("p1 or p2 is none")
    return -1

  #DECKS
  decks = db["decks"].keys()
  if d1name not in decks or d2name not in decks:
    print("d1 or d2 is none")
    return -1

  p1db = db[str(p1.id)]
  p2db = db[str(p2.id)]

  p1db['D2P'] = d1name
  p2db['D2P'] = d2name

  db[str(p1.id)] = p1db
  db[str(p2.id)] = p2db
  
  gain = elo(p1.id, p2.id)
  await message.channel.send(gain)