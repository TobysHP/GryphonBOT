import discord 
from replit import db
import matplotlib.pyplot as plt
import numpy as np
import player as pl

async def lineup(client: discord.Client, message: discord.Message):
  index = 0
  words = message.content.split()
  if len(words)!=16:
    await message.channel.send("Le format est incorrecte")
    return -1
  embed = discord.Embed(title="Line Up vs {}".format(words[1]), color=0xf5a816)
  embed.add_field(
              name="Date",
              value="{} {} ".format(words[2],words[3]),
              inline=False)
  embed.add_field(
              name="Main LU",
              value="{}: {} \n{}: {} \n{}: {} \n{}: {}\n{}: {}".format(words[4],words[5], words[6], words[7], words[8], words[9], words[10], words[11], words[12], words[13]),
              inline=False)
  embed.add_field(
              name="Sub",
              value="{}: {} ".format(words[14],words[15]),
              inline=False)
  embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775659509233614881/779078160313876560/Sans-titre-1.png")
  
  
  msg = await message.channel.send(embed=embed)
  await msg.add_reaction("✅")
  await msg.add_reaction("❌")

async def luProcess(client: discord.Client, reaction, embeds):
  channel = client.get_channel(775659410139643925)
  bis = client.get_channel(798113614531395614)
  check = False
  reactions = reaction.message.reactions
  for reac in reactions:
    if reac.emoji == '✅':
      if reac.count > 1:
        check = True
    if reac.emoji == "❌":
      if reac.count > 1:
        check = False
  if check:
    await channel.send(embed = embeds[0])
    await reaction.message.delete()
    ping = await channel.send(reaction.message.guild.default_role)
    await ping.delete()

  
