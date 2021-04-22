import discord 
from replit import db
import functions as fnct 
import asyncio

##################################
## COMMANDES LIEES AUX TOURNOIS ##
##################################

async def create(client: discord.Client, message: discord.Message):
  db["tour"] = {"joueurs":[], "points":[], "tb":[]}