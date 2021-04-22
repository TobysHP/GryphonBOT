import discord
import os
import player as pl
import lobby as lo
import decks as de
import lineup as lu
import sheet
import sys
import functions as f
from replit import db
from keep_alive import *
import numpy as np
import gspread
from pprint import pprint
import math
from oauth2client.service_account import ServiceAccountCredentials

client = discord.Client()


@client.event
async def on_ready():
  print('Ready as {0.user}'.format(client)) 

@client.event
async def on_message(message):
  try:
    prefix = message.content[0]
  except:
    return -1
  if prefix == '!':
    mess = message.content[1:]
    i = 0
    for char in mess:
      if char == " ":
        mess = mess[:i]
        break
      i += 1

    print(mess)

    if mess == "h" or mess == "help":

      ##################
      ## HELP COMMAND ##
      ##################

      embed = discord.Embed(title="Documentation", color=0xf5a816)
      embed.add_field(name="!p ou !participate", value="Permet de s'inscrire à la Gryphon League", inline=False)
      embed.add_field(name="!sd ou !setDeck", value="Permet d'enregistrer un deck'", inline=False)
      embed.add_field(name="!deck ou !decks", value="Permet de voir les decks jouable", inline=False)
      embed.add_field(name="!c ou !can", value="Permet de s'inscrire dans un lobby", inline=False)
      embed.add_field(name="!d ou !drop", value="Permet de se retirer d'un lobby", inline=False)
      embed.add_field(name="!l ou !list", value="Permet de regarder la liste des lobby", inline=False)
      embed.add_field(name="!w ou !win", value="Permet de se déclarer vainqueur de son lobby", inline=False)
      embed.add_field(name="!ld ou !leaderboard", value="Permet de visualiser le classement", inline=False)
      embed.add_field(name="!me", value="Permet de visualiser ses stats", inline=False)
      embed.add_field(name="!stat [joueur] [joueur] ...", value="Permet de visualiser les stats de un ou plusieurs joueurs", inline=False)
      embed.add_field(name="!sheet", value="Permet d'update la feuille des matchup ainsi que d'avoir le lien", inline=False)
      await message.channel.send(embed=embed)
      "updateSheet"
    

    ################################
    ## COMMANDES LIEES  AUX LOBBY ##
    ################################
    elif mess == "c" or mess == "can":
      await lo.can(client, message)
    elif mess == "d" or mess == "drop":
      await lo.drop(client, message)
    elif mess == "l" or mess == "list":
      await lo.listOfLobbies(client, message)


    #################################
    ## COMMANDES LIEES AUX JOUEURS ##
    #################################

    elif mess == "p" or mess == "participate":
      await pl.participate(client, message)
    elif mess == "ld" or mess == "leaderboard":
      await pl.leaderboard(client, message)
    elif mess == "w" or mess == "win":
      await pl.win(client, message)
    elif mess == "me" or mess == "stat":
      await pl.stat(client, message)


    ###############################
    ## COMMANDES LIEES AUX DECKS ##
    ###############################

    elif mess == "sd" or mess == "setDeck":
      await de.setDeck(client, message)

    elif mess == "deck" or mess == "decks":
      await de.decks(client, message)

    elif mess == "plot":
      await de.plotDecks(client, message)


    ################################
    ## COMMANDES LIEES A LA SHEET ##
    ################################

    elif mess == "sheet":
      try:
        sheet.updateDatas()
        await message.channel.send("https://docs.google.com/spreadsheets/d/14iz0t1vsWijLT6t219XanYJkplIizeNlEKFtti-ZxHE/edit#gid=148969983")

      except:
        pass

    ################################
    ## COMMANDES LIEES AUX LINEUP ##
    ################################

    elif mess == "lu":
      await lu.lineup(client, message)

    else:
      await message.channel.send("Cette commande n'existe pas")


    ###############################
    ## FIN DES COMMANDES PUBLIC  ##
    ###############################

  if prefix == '?' and message.author.id == 384723399718469634:
    mess = message.content[1:]
    i = 0
    for char in mess:
      if char == " ":
        mess = mess[:i]
        break
      i += 1

    print(mess)

    ########################
    ## COMMANDES PRIVEES  ##
    ########################

    if mess == "match":
      await f.manualMatch(client, message)
      
    if mess == "saveDB":
      await f.saveDataBase(client, message)

    if mess == "setDB":
      await f.setDataBase(client,message)
    
    if mess == "addDeck":
      await de.addDeck(client, message)



      



###################################
## COMMANDES LIEES AUX REACTIONS ##
###################################

@client.event
async def on_reaction_add(reaction, user):
  if reaction.message.author.id == 801481576336064562:
    embeds = reaction.message.embeds
    if embeds[0].to_dict()['title'] == "Close lobby":
      await pl.winProcess(client, reaction, embeds)

    if "Line Up" in embeds[0].to_dict()['title']:
      await lu.luProcess(client, reaction, embeds)
  
#del db["384723399718469634"]



#reset database

'''keys = db.keys()
for key in keys:
  del db[key]
  #print(key, db[key])

db["lobby"] = {"players":[[]],"close":[[]]}

db["decks"] = {}
db["mat"] = []

for row in db['mat']:
  print(row)

db["lobby"] = {"players":[[]],"close":[[]]}
db["decks"] = {}
db["mat"] = []
keys = db.keys()
for key in keys:
  print(key, db[key])
'''


#################################
####  GOOGLE SHEET ##############
#################################

'''scope = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client_sheets = gspread.authorize(creds)

sheet = client_sheets.open("GLFgryphons").worksheet("MU datas")  # Open the spreadhseet


for deck in db["decks"].keys():
  sheet.update_cell(2*int(db["decks"][deck]) + 2, 1, deck)
  sheet.update_cell(1, int(db["decks"][deck]) + 2, deck)


mat = np.array(db["mat"])
matcopy = np.copy(mat)
matcopy2 = np.copy(mat)

[n, m] = np.shape(mat)

matcopy = matcopy.tolist()
matcopy2 = matcopy2.tolist()

for i in range(n):
  for j in range(m):
    matcopy[i][j] = round(mat[i][j]/(mat[i][j] + mat[j][i]),4)
    if mat[i][j] + mat[i][j] == 0:
      matcopy[i][j] = 'no data'

    matcopy2[i][j] = "{} - {}".format(mat[i][j], mat[j][i])


finalMat = []
for i in range(n):
  finalMat.append(matcopy[i])
  finalMat.append(matcopy2[i])


sheet.update('B2', finalMat)'''


keep_alive()
client.run(os.getenv('TOKEN'))



