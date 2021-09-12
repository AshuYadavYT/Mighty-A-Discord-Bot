import discord
from discord.ext import commands, tasks
from datetime import datetime
import os
from keep_alive import keep_alive
from discord_slash import SlashCommand
from discord.ext.commands.core import has_permissions, has_role
import random
from discord.ext.commands.errors import MissingPermissions, BotMissingPermissions, MissingRequiredArgument, BadArgument, CommandInvokeError, CommandOnCooldown, MissingRole
import config
import time
import requests
import wikipedia
from mojang import MojangAPI

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=config.prefix, case_insensitive=True, intents=intents)
client.remove_command("help")
slash = SlashCommand(client, sync_commands=True)
client.launch_time = datetime.utcnow()


cl = config.colour 
owner = client.get_user(config.owner)


@client.event
async def on_ready():
    print("I am online")

@client.event
async def on_member_join(member):
  channel = client.get_channel(804653115918909443)
  await channel.send(f"{member.mention} Aapka Yaha Dil Se Sawagat hai <a:HeartGIF:876002290497093632> ")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f"Young {ctx.message.author.mention} your Quirk is not grown yet! You can't use this command.")
    elif isinstance(error, BotMissingPermissions):
        await ctx.send(f"I don't have enough permissions to do that")

@client.event
async def on_guild_join(guild):
        joinchannel = guild.system_channel
        embed=discord.Embed(title="**It is fine now. Why? because i am here!**:muscle:", description="Thanks for inviting me ", color=0)
        await joinchannel.send(embed=embed)

#======================================================================================================================
#Fun and Info
#======================================================================================================================
@client.command()
async def ping(ctx):
    embed=discord.Embed(description=f"Pong! - {round(client.latency * 1000)}ms", color=cl)
    await ctx.reply(embed=embed)

@client.command()
async def info(ctx):
    delta_uptime = datetime.utcnow() - client.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    embed=discord.Embed(title="My Stats", color=cl)
    embed.add_field(name="**Ram**", value="`4GB`", inline=True)
    embed.add_field(name="**Ping**", value=f"`{round(client.latency * 1000)}ms`", inline=True)
    embed.add_field(name="**Uptime**", value=f"`{days}d, {hours}h, {minutes}m, {seconds}s`", inline=True)
    embed.add_field(name="**Language**", value="`Python`", inline=True)
    embed.add_field(name="**Owner**", value="`YTAGaming#4250`", inline=True)
    embed.set_thumbnail(url="https://media1.tenor.com/images/508fe7a0908b87ea1de36391094a1049/tenor.gif")
    embed.set_footer(text="Open-source bot")

    await ctx.reply(embed=embed)

@client.command()
async def uptime(ctx):
    delta_uptime = datetime.utcnow() - client.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.reply(f"I am running from `{days}d, {hours}h, {minutes}m, {seconds}s`")

@client.command()
async def wiki(ctx, *, search):
    await ctx.send(f'Searching Results for `{search}`', delete_after=1)

    try:
        wikipedia.set_lang("en")
        embed = discord.Embed(title=f"{wikipedia.page(search).title}", description=wikipedia.summary(search, sentences=3), color=cl)
        embed.add_field(name=f'Read More..', value=f'[Click Here]({wikipedia.page(search).url})')
        embed.set_image(url=f"{wikipedia.page(search).images[1]}")
        embed.set_footer(text=f"Requested By {ctx.message.author}")

        await ctx.reply(embed=embed)

    except:
        print('Not Found')
        await ctx.send(f'Results Not Found Maybe You Mean **{wikipedia.suggest(search)}**')

@wiki.error
async def wiki_error(ctx, error):
  if isinstance(error, MissingRequiredArgument):
    await ctx.reply(f"Example- `+wiki Python`")

@client.command()
async def joke(ctx):
  joke = requests.get('https://some-random-api.ml/joke')
  random_joke = joke.json()
  await ctx.reply(f"{random_joke['joke']}")

@client.command()
async def dog(ctx):
    dogeapi = requests.get("https://dog.ceo/api/breeds/image/random")
    dog = dogeapi.json()
    embed = discord.Embed(title="I Love Dog's", color=cl)
    embed.set_image(url=f"{dog['message']}")

    await ctx.reply(embed=embed)

@client.command()
async def cat(ctx):
  catapi = requests.get('https://some-random-api.ml/img/cat')
  cat = catapi.json()
  embed = discord.Embed(title="Meow ?", color=cl)
  embed.set_image(url=f'{cat["link"]}')
  await ctx.reply(embed=embed)

@client.command()
async def inspire(ctx):
    quoatesapi = requests.get("https://api.quotable.io/random")
    quotes = quoatesapi.json()
    await ctx.reply(f"**{quotes['content']}**\n\t     *-{quotes['author']}*")

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def skin(ctx, *, Name):
  fetch_user = MojangAPI.get_uuid(Name)
  profile = MojangAPI.get_profile(fetch_user)

  embed = discord.Embed(title=f"Skin of {Name}", description=f"Want to Download? [click here]({profile.skin_url})", color=0x2ecc71)
  embed.set_image(url=profile.skin_url)
  await ctx.reply(embed=embed)

@skin.error
async def skin_error(ctx, error):
  if isinstance(error, CommandInvokeError):
    await ctx.send(f"Skin not found make sure you entered correct Gamertag!")
  elif isinstance(error, MissingRequiredArgument):
    embed = discord.Embed(title="Minecraft Player Skin Stealer :eyes:", description="Usage - `skin YTAGaming4250`\nCase Sensitive!\nRequirements - Minecraft Java Account!", color=0x2ecc71)
    await ctx.send(embed=embed)
  elif isinstance(error, CommandOnCooldown):
    await ctx.send(f"Cooldown Young {ctx.message.author.name}, Try again after `{error.retry_after:.2f}s`", delete_after=5)

#Fun and Info Slash Version
@slash.slash(name="Uptime", description="Shows bot running time")
async def suptime(ctx):
    delta_uptime = datetime.utcnow() - client.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.reply(f"I am running from `{days}d, {hours}h, {minutes}m, {seconds}s`")

@slash.slash(name="Joke", description="Savage Dad Jokes")
async def sjoke(ctx):
  joke = requests.get('https://some-random-api.ml/joke')
  random_joke = joke.json()
  await ctx.send(f"{random_joke['joke']}")

@slash.slash(name="Poke", description="Random Pokemon Photos")
async def spokemon(ctx):
    embed=discord.Embed(title="Some Pokemons", color=cl)
    embed.set_image(url=f"https://images.pokecord.xyz/regular/{random.randint(1, 807)}.png")
    await ctx.send(embed=embed)

@slash.slash(name="Dog", description="Some Random dogs")
async def sdoge(ctx):
    dogeapi = requests.get("https://dog.ceo/api/breeds/image/random")
    dog = dogeapi.json()
    embed = discord.Embed(title="I Love Dog's", color=cl)
    embed.set_image(url=f"{dog['message']}")

    await ctx.send(embed=embed)

@slash.slash(name="Cat", description="Some Random Cats")
async def scat(ctx):
  catapi = requests.get('https://some-random-api.ml/img/cat')
  cat = catapi.json()
  embed = discord.Embed(title="Meow ?", color=cl)
  embed.set_image(url=f'{cat["link"]}')
  await ctx.send(embed=embed)

@slash.slash(name="Inspire", description="Never Give Up!")
async def sinspire(ctx):
    quoatesapi = requests.get("https://api.quotable.io/random")
    quotes = quoatesapi.json()
    await ctx.send(f"**{quotes['content']}**\n\t     *-{quotes['author']}*")

    if (quoatesapi == 404):
        await ctx.send("Error please try again later")

@slash.slash(name="Ping", description="Shows bot latency")
async def pong(ctx):
    await ctx.send(f'Pong! - {round(client.latency * 1000)}ms')

@slash.slash(name="Info", description="Information about me XD")
async def sinfo(ctx):
    delta_uptime = datetime.utcnow() - client.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    embed = discord.Embed(title="My Stats", color=cl)
    embed.add_field(name="**Ram**", value="`4GB`", inline=True)
    embed.add_field(name="**Ping**", value=f"`{round(client.latency * 1000)}ms`", inline=True)
    embed.add_field(name="**Uptime**", value=f"`{days}d, {hours}h, {minutes}m, {seconds}s`", inline=True)
    embed.add_field(name="**Language**", value="`Python`", inline=True)
    embed.add_field(name="**Owner**", value="`YTAGaming#4250`", inline=True)
    embed.set_footer(text="Open-source bot")

    await ctx.send(embed=embed)

@client.command()
async def avatar(ctx, member : discord.Member):
  embed=discord.Embed(title="Nice!")
  embed.set_image(url=f"{member.avatar_url}")
  await ctx.send(embed=embed)

@avatar.error
async def avatar_error(ctx, error):
  if isinstance(error, MissingRequiredArgument):
    embed=discord.Embed(title="Nice!")
    embed.set_image(url=f"{ctx.message.author.avatar_url}")
    await ctx.send(embed=embed)

@client.command()
async def dm(ctx, member : discord.Member,* , message):
  try:
    embed = discord.Embed(title=f"Hello {member.name}!", description=f"You Got Message from {ctx.message.guild.name} Server")
    embed.add_field(name="Message", value=message, inline=False)
    await member.send(embed=embed)
    await ctx.reply(f"Message Sucessfully sent to {member.name}\nID - {member.id}")
  except:
    await ctx.reply(f"Their Dm's is off i can't send message.")

@client.command()
@has_role(804926508677333053)
async def change_status(ctx,* , name):
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{name}"))
  await ctx.send(f"I changed my presence to `{name}`")

@change_status.error
async def error_status(ctx, error):
  if isinstance(error, MissingRole):
    await ctx.reply(f"{ctx.message.author.name} Only my Owner can use this command.")

#======================================================================================================================
#Moderation Commands Starts from here
#======================================================================================================================

@client.command()
@has_permissions(manage_messages=True)
async def purge(ctx, amount=2):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"Done Young{ctx.message.author.mention}", delete_after=5)

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason= "None"):
    if member == ctx.message.author:
        await ctx.send('Bruh, why you wanna kick your self ;)')

    await member.kick(reason=reason)

    embed = discord.Embed(title="Texas Smash!", description=f"Sucessfully kicked {member.mention}\n `Reason: {reason}`", color=cl)
    embed.set_author(name=f"", icon_url=f"{ctx.message.author.avatar_url}")
    embed.set_thumbnail(url="https://media1.tenor.com/images/026142d2bb5d257b8f5c311ac44c28db/tenor.gif")
    embed.set_footer(text=f"By {ctx.message.author}")

    await ctx.send(embed=embed)

    try:
       await member.send(f"You have been kicked from **{ctx.message.guild.name}** \n`Reason : {reason}`!")

    except:
        print("User Dm's is off")


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send(f"Please mention or give user id you want to kick.\n Example:`+kick Dabi <reason : optional>`")
    elif isinstance(error, BadArgument):
        await ctx.send(f"Young {ctx.message.author} Error:`Member not found`")


@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason= "None"):
    if member == ctx.message.author:
        await ctx.send('Why you wanna ban your self ?')
        

    await member.ban(reason=reason)
    embed = discord.Embed(title="Go Beyond!", description=f"Successfully Banned {member.mention}!\n`Reason : {reason}`", color=cl)
    embed.set_thumbnail(url="https://media1.tenor.com/images/eee6e1af614d09a91c23e778c1a0dda4/tenor.gif")
    embed.set_footer(text=f"By {ctx.message.author}")
    await ctx.send(embed=embed)

    try:
        await member.send(f"You have been Banned from **{ctx.message.guild.name}!**\n`Reason : {reason}`")

    except:
        print("User Dms is off")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send(f"Please mention or give user id you want to ban.\n Example:\n`+ban Mineta <reason : As you already know>`")
    elif isinstance(error, BadArgument):
        await ctx.send(f"Young {ctx.message.author} Error:`Member not found`")
@client.command()
@has_permissions(ban_members=True)
async def unban(ctx, member : discord.Member, *, user):
    await member.unban(user=user)
    await ctx.send(f"Unbaned {user}")


@client.command()
async def report(ctx, *, reason):
    channel = client.get_channel(860346334832623656)
    embed = discord.Embed(title="", description=f"Sent by `{ctx.message.author}` from server `{ctx.message.guild.name}`\n`Message : {reason}`", color=cl)
    embed.set_thumbnail(url=f"{ctx.message.author.avatar_url}")
    embed.set_footer(text="Mighty")

    await channel.send(embed=embed)

client.run(config.token)
