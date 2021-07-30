# imports
import discord # importing API wrapper
from discord import user # importing API wrapper 
from discord.client import Client # importing client
from discord.ext import commands # importing commands
import os # for reading and importing files
import sys # for exit 
import json # importing json for custom prefixes and warning system
import random # for 8ball command 
import asyncio # for mute command

# intents 
intents = discord.Intents.default()
intents.members = True 

# getting prefixes 
def get_prefix(client, message):
    with open("config/customprefix.json", "r") as p: # opens the customprefix json file 
        # variables to declare
        prefixes = json.load(p) # loads the customprefix json file 
    return prefixes[str(message.guild.id)] # returns the contents of the customprefix json file 

# creating the bot 
client = commands.Bot(command_prefix=get_prefix, intents=intents, case_insensitive=True, help_command=None) # creating the client
client.sniped_messages = {} # for snipe command 

# defaulting prefix on guild join
@client.event
async def on_guild_join(guild):
    with open("config/customprefix.json", "r") as p: # opens the customprefix json file 
        prefixes = json.load(p) # loads the customprefix json file 
    
    # variables to declare
    prefixes[str(guild.id)] = "£" # defualt prefix

    with open("config/customprefix.json", "w") as p:
        json.dump(prefixes,p)

# lists
responses = [ # for the magic 8ball command
        "it is certain", "it is decidedly so.", "without a doubt",
        "yes - definitely", "you may rely on it", "as I see it, yes",
        "most likely", "outlook good", "yes", "signs point to yes",
        "don't count on it", "my reply is no", "my sources say no",
        "outlook not so good", "very doubtful", "suck your mother"
] 

configFiles = { # for reading config files
    "botToken" : "config/bot-token",
    "apiKey" : "config/api-key",
    "welcomeID" : "config/welcomechannel-id",
    "goodbyeID" : "config/goodbyechannel-id"
}

mutedTime = { # for the mute command
    "1m" : 60,
    "5m" : 300,
    "10m" : 600,
    "30m" : 1800,
    "1h" : 3600,
    "2h" : 7200,
    "6h" : 21600,
    "12h" : 43200,
    "24h" : 86400
}

# config file reading
if os.path.exists(configFiles["botToken"]): # for bot token
    # reading file
    with open(configFiles["botToken"], "r") as bottokenconfigFile:
        # variables to declare 
        global token
        token = bottokenconfigFile.read().strip('\n')

if os.path.exists(configFiles["welcomeID"]): # for welcome message
    # reading file
    with open(configFiles["welcomeID"], "r") as welcomeidFile:
        # variables to declare 
        global welcomechannelID
        welcomechannelID = welcomeidFile.read().strip('\n')

if os.path.exists(configFiles["goodbyeID"]): # for goodbye message
    # reading file
    with open(configFiles["goodbyeID"], "r") as goodbyeidFile:
        # variables to declare 
        global goodbyechannelID
        goodbyechannelID = goodbyeidFile.read().strip('\n')

else:
    # error message
    print(f"the config/bot-token file is missing, please create it or comment out this code")
    # exit
    sys.exit()

if os.path.exists(configFiles["apiKey"]): # for dog command
    # imports
    import dogApi
    import catApi
    # reading file
    with open(configFiles["apiKey"], "r") as apikeyFile:
        # variables to declare
        global apiKey
        apiKey = apikeyFile.read().strip('\n')
else:
    # error message
    print(f"the config/api-key file is missing, please create it or comment out this code")
    # exit
    sys.exit()

# warning system
with open("config/warns.json", encoding="utf-8") as warnsJson : # opening warns.json file
    try:
        # variables to declare
        warns = json.load(warnsJson)
    except ValueError:
        # variables to declare
        warns = {}
        warns["users"] = []

# on ready 
@client.event
async def on_ready():
    # logging in
    print(f"logged in as {client.user.name}#{client.user.discriminator}!") # if this message prints, the bot is working
    # variables to declare
    activity = discord.Game(name="£cmds") # the name of the activity can be changed to anything you like
    status = discord.Status.online # online can be swapped with: "idle", "offline", "dnd (do_not_disturb)"
    # setting presence
    await client.change_presence(status=status, activity=activity) # changes presence for the bot

# help
@client.command(aliases=["help"])
async def cmds(ctx):
    # variables to declare
    author = ctx.author
    channel = await author.create_dm() # creates a DM with the context author 
    with open("config/customprefix.json", "r") as p: # opens the customprefix json file 
        prefixes = json.load(p) # loads the customprefix json file 
    prefix = prefixes[str(ctx.guild.id)]
    # embed
    helpEmbed = discord.Embed(title='***HELP***') # creating an embed for the help command 
    helpEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed
    helpEmbed.set_thumbnail(url=author.avatar_url) # adding an thumbnail to the embed
    helpEmbed.add_field(name="ping", value=f"type {prefix}ping to see the bot latency!", inline = False) # adding a field to the embed
    helpEmbed.add_field(name="prefix", value="if you want to see the current prefix, ping the bot!", inline = False) # adding a field to the embed
    helpEmbed.add_field(name="avatar", value=f"type {prefix}avatar, or {prefix}av, to get your own avatar embedd, or you can ping another server member as an argument, for their avatar!", inline = False) # adding a field to the embed
    helpEmbed.add_field(name="8ball", value=f"type {prefix}8ball and a question to ask the magic 8 ball!", inline = False) # adding a field to the embed
    helpEmbed.add_field(name="dog", value=f"type {prefix}dog(e) to get a random image of a a dog, credit to https://thedogapi.com", inline = False) # adding a field to the embed
    helpEmbed.add_field(name="cat", value=f"type {prefix}cat to get a random image of a a cat, credit to https://thecatapi.com", inline = False) # adding a field to the embed
    helpEmbed.add_field(name="userinfo", value=f"type {prefix}userinfo to get info about yourself, or you can ping another member of the server as an argument, to find info about them!", inline = False) # adding a field to the embed
    helpEmbed.add_field(name="serverinfo", value=f"type {prefix}serverinfo to get info about your server!", inline = False) # adding a field to the embed
    helpEmbed.add_field(name="botinfo", value=f"type {prefix}botinfo to get info about my bot!", inline = False) # adding a field to the embed
    helpEmbed.add_field(name="mute", value=f"type {prefix}mute, the user, then the time, then a reason, or not, to mute a member form your server! (automatic unmuting)") # adding a field to the embed
    helpEmbed.add_field(name="unmute", value=f"type {prefix}unmute, the user, to unmute a member from your server! (only needed if automatic unmute fails)") # adding a field to the embed
    helpEmbed.add_field(name="changeprefix", value=f"type {prefix}changeprefix, then give an argument (this will be your new prefix)!", inline = False) # adding a field to the embed
    helpEmbed.add_field(name="ban", value=f"type {prefix}ban, the user, then a reason, or not, to ban a member from your server!") # adding a field to the embed
    helpEmbed.add_field(name="unban", value=f"type {prefix}unban, the banned user's name and discriminator seperated by '#', to unban a member from your server!") # adding a field to the embed
    helpEmbed.add_field(name="kick", value=f"type {prefix}kick, the user, then a reason, or not, to kick a member from your server!", inline = False) # adding a field to the embed
    helpEmbed.add_field(name="warn", value=f"type {prefix}warn, the user, then a reason, or not, to warn a member of your server!") # adding a field to the embed
    helpEmbed.add_field(name="warnings", value=f"tpye {prefix}warnings, the user, to find out the amount of warnings a user has, if no embed is sent, the user has no warns") # adding a field to the embed
    # sends content 
    await channel.send(embed=helpEmbed) # DMs the embed we just made  

# events
@client.event
async def on_message(message):
    try:
        if message.mentions[0] == client.user:
            with open("config/customprefix.json", "r") as p:
                prefixes = json.load(p)
            # variables to declare
            prefix = prefixes[str(message.guild.id)] 

            await message.channel.send(f"the current prefix for this server is {prefix}")
    except:
        pass
    # sends content
    await client.process_commands(message)

@client.event
async def on_member_join(member):
    # variables to declare
    channel = client.get_channel(int(welcomechannelID)) # channel id from config/welcomechannel-id as an integer
    # embed
    welcomeEmbed = discord.Embed(title=f"{member.name}#{member.discriminator} welcome to {member.guild}") # creationg an embed for the welcome message 
    welcomeEmbed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url) # adding an author to the embed
    # sends content
    await channel.send(embed=welcomeEmbed) # sends the embed we just made 

@client.event
async def on_member_remove(member):
    # variables to declare
    channel = client.get_channel(int(goodbyechannelID)) # channel id from config/goodbyechannel-id as an integer
    # embed
    goodbyeEmbed = discord.Embed(title=f"{member.name}#{member.discriminator} has left {member.guild}") # creationg an embed for the welcome message 
    goodbyeEmbed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url) # adding an author to the embed
    # sends content
    await channel.send(embed=goodbyeEmbed) # sends the embed we just made 

@client.event
async def on_message_delete(message):
    if message.attachments:
        # variables to declare 
        image = message.attachments[0]
        client.sniped_messages[message.guild.id] = (image.proxy_url, message.content, message.author, message.channel.name, message.created_at) # on message delete, this info is sniped 
    else:
        # variables to declare
        client.sniped_messages[message.guild.id] = (message.content,message.author, message.channel.name, message.created_at) # on message delete, this info is sniped 

# moderation commands
@client.command()
@commands.has_permissions(administrator=True, manage_guild=True) # permissions check 
async def changeprefix(ctx, prefix):
    with open("config/customprefix.json", "r") as p: # opens the customprefix json file 
        prefixes = json.load(p) # loads the customprefix json file 
    
    # variables to declare
    prefixes[str(ctx.guild.id)] = prefix # defualt prefix
    
    with open("config/customprefix.json", "w") as p:
        json.dump(prefixes, p)
    # sends content
    await ctx.channel.send(f"{ctx.author} changed the prefix for this server to {prefix}")

@client.command()
@commands.has_permissions(administrator=True, kick_members=True) # permissions check
async def kick(ctx, member : discord.Member, *, reason = None):
    # variables to declare 
    author = ctx.author
    # kick
    await member.kick(reason=reason)
    # embed
    kickEmbed = discord.Embed(title=f"{member.name}#{member.discriminator} was kicked by {author.name}#{author.discriminator} :boom:") # creating an embed for the kick command 
    kickEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed 
    kickEmbed.add_field(name="reason", value=f"{reason}", inline = False) # adding a field to the embed
    # sends content
    await ctx.send(embed=kickEmbed) # sends the embed we just made

@client.command()
@commands.has_permissions(administrator=True, ban_members=True) # permissions check
async def ban(ctx, member : discord.Member, *, reason = None):
    # variables to declare 
    author = ctx.author
    # ban
    await member.ban(reason=reason, delete_message_days=0)
    # embed
    banEmbed = discord.Embed(title=f"{member.name}#{member.discriminator} was banned by {author.name}#{author.discriminator} :boom:") # creating an embed for the ban command 
    banEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed
    banEmbed.add_field(name="reason", value=f"{reason}", inline = False) # adding a field to the embed
    # sends content
    await ctx.send(embed=banEmbed) # sends the embed we just made

@client.command()
@commands.has_permissions(administrator=True, ban_members=True) # # permissions check
async def unban(ctx, *, member):
    # variables to declare
    author = ctx.author
    usersBanned = await ctx.guild.bans()
    memberName, memberDiscriminator = member.split('#')
    # searching through ban entries 
    for banEntry in usersBanned:
        # variables to declare
        user = banEntry.user
    # if statement
    if(user.name, user.discriminator) == (memberName, memberDiscriminator):
        # unban
        await ctx.guild.unban(user)
        # embed
        unbanEmbed = discord.Embed(title=f"{user.name}#{user.discriminator} was unbanned by {author.name}#{author.discriminator}") # creating an embed for the unban command
        unbanEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed 
        # sends content
        await ctx.send(embed=unbanEmbed) # sends the embed we just made

@client.command()
@commands.has_permissions(administrator=True, kick_members=True, ban_members=True, manage_roles=True) # permissions check
async def warn(ctx, user: discord.User, *, reason = None):
    for currentMember in warns["users"]:
        if currentMember["name"] == user.name:
            currentMember["reasons"].append(reason)
            break
    else:
        warns["users"].append({
            "name" : user.name,
            "reasons" : [reason]
        })
    with open("config/warns.json", "w") as warnWrite:
        json.dump(warns,warnWrite)
    # variables to declare
    author = ctx.author
    # embed
    warnEmbed = discord.Embed(title=f"{user.name}#{user.discriminator} was warned by {author.name}#{author.discriminator}") # creating an embed for the warn command
    warnEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed
    warnEmbed.add_field(name="reason", value=f"{reason}", inline = False) # adding a field to the emed
    # sends content 
    await user.send(embed=warnEmbed) # DMs the user the embed we just made
    await ctx.send(embed=warnEmbed) # sends the embed we just made 

@client.command()
@commands.has_permissions(administrator=True, kick_members=True, ban_members=True, manage_roles=True) # permissions check
async def warnings(ctx, user: discord.User):
    for currentMember in warns["users"]:
        if(user.name == currentMember["name"]):
            # variables to declare
            author = ctx.author
            # embed
            warningsEmbed = discord.Embed(title=f"warnings for {user.name}#{user.discriminator}") # creating an embed for the warnings command
            warningsEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed
            warningsEmbed.set_thumbnail(url=user.avatar_url) # adding a thumbnail to the embed
            warningsEmbed.add_field(name="warnings", value=f"{user.name}#{user.discriminator} is on {len(currentMember['reasons'])} warnings") # adding a field to the embed
            # sends content
            await ctx.send(embed=warningsEmbed) # sends the embed we just made

@client.command()
@commands.has_permissions(administrator=True, kick_members=True, ban_members=True, manage_roles=True, manage_messages=True) # permissions check
async def mute(ctx, member: discord.Member, time, *, reason = None):
    # variables to declare 
    server = ctx.guild
    author = ctx.author
    mutedRole = discord.utils.get(server.roles, name="muted") # looks for muted role
    # if muted role doesn't exist
    if not mutedRole:
        mutedRole = await server.create_role(name="muted") # creates muted role
    for channel in server.channels:
        await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True) # sets muted role permissions
    # mute
    await member.add_roles(mutedRole, reason=reason) # adds muted role
    time=int(mutedTime[time])
    # embed
    mutedEmbed = discord.Embed(title=f"{member.name}#{member.discriminator} was muted by {author.name}#{author.discriminator}") # creating an embed for the mute command
    mutedEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed
    mutedEmbed.add_field(name="reason", value=f"{reason}") # adding a field to the embed
    mutedEmbed.add_field(name="duration", value=f"{time}s") # adding a field to the embed
    # sends content
    await member.send(embed=mutedEmbed) # DMs the member the embed we just made
    await ctx.send(embed=mutedEmbed) # sends the embed we just made 
    # mute time 
    await asyncio.sleep(time) # timer
    # unmute
    await member.remove_roles(mutedRole) # removes muted role
    # embed
    unmuteEmbed = discord.Embed(title=f"{member.name}#{member.discriminator}'s mute has ended") # creating an embed for the automatic unmute stage
    unmuteEmbed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url) # adding an author to the embed
    # sends content
    await member.send(embed=unmuteEmbed) # DMs the member the embed we just made 

# manual unmute 
@client.command()
@commands.has_permissions(administrator=True, kick_members=True, ban_members=True, manage_roles=True, manage_messages=True) # permissions check
async def unmute(ctx, member: discord.Member):
    # variables to declare
    server = ctx.guild
    author = ctx.author
    mutedRole = discord.utils.get(server.roles, name = "muted") # looks for muted role
    # unmute
    await member.remove_roles(mutedRole) # removes muted role
    # embed 
    manualunmuteEmbed = discord.Embed(title=f"{member.name}#{member.discriminator} was unmuted by {author.name}#{author.discriminator}") # creating an embed for the manual unmute command 
    manualunmuteEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed 
    # sends content
    await member.send(embed=manualunmuteEmbed) # DMs the user the embed we just made 
    await ctx.send(embed=manualunmuteEmbed) # sends the embed we just made 

# general commands
@client.command()
async def ping(ctx):
    # variables to declare
    author = ctx.author
    botLatency = client.latency*1000
    # embed
    pingEmbed = discord.Embed(title='ping') # creating an embed for the ping command 
    pingEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed
    pingEmbed.add_field(name="bot latency", value=f"{round(botLatency)}ms!") # adding a field to the embed
    # sends content
    await ctx.send(embed=pingEmbed) # sends the embed we just made 

@client.command(aliases=['av'])
async def avatar(ctx, *, avamember: discord.Member = None):
    if(avamember == None): # if there is no argument given, it fetches the avatar of the context author
        # variables to declare
        author = ctx.author
        # embed
        avatarEmbed = discord.Embed(title=f"avatar of {author.name}#{author.discriminator}") # creating the avatar embed
        avatarEmbed.set_image(url=author.avatar_url) # embedding the author's profile picture
        # sends content
        await ctx.send(embed=avatarEmbed) # sends the embed we just made 
    else:
        # embed
        avatarEmbed = discord.Embed(title=f"avatar of {avamember.name}#{avamember.discriminator}") # creating the avatar embed
        avatarEmbed.set_image(url=avamember.avatar_url) # embedding the user's profile pciture 
        # sends content
        await ctx.send(embed=avatarEmbed) # sends the embed we just made 

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    # variables to declare
    author = ctx.author 
    # embed
    ballEmbed = discord.Embed(title="8ball") # creating an embed for the 8ball command 
    ballEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed 
    ballEmbed.add_field(name = "question", value = f"{question}", inline = False) # adding a field to the embed
    ballEmbed.add_field(name = "answer", value = f"{random.choice(responses)}", inline = False) # adding a field to the embed
    # sends content
    await ctx.send(embed=ballEmbed) # sends the embed we just made

@client.command()
async def userinfo(ctx, *, userinfo: discord.Member = None):
    if(userinfo == None): # if there is no argument given, it fetches userinfo of the context author
        # variables to declare
        author = ctx.author
        # embed
        userinfoEmbed = discord.Embed(title=f"{author.name}", description="information we've received!") # creating an embed for the userinfo command 
        userinfoEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed 
        userinfoEmbed.set_thumbnail(url=author.avatar_url) # adding an thumbnail to the embed
        userinfoEmbed.add_field(name="name", value=f"{author.name}#{author.discriminator}", inline = False) # adding a field to the embed
        userinfoEmbed.add_field(name="nickname", value=f"{author.nick}", inline = False) # adding a field to the embed
        userinfoEmbed.add_field(name="id", value=f"{author.id}", inline = False) # adding a field to the embed
        userinfoEmbed.add_field(name="account creation", value=f"{author.created_at}", inline = False) # adding a field to the embed
        # sends content
        await ctx.send(embed=userinfoEmbed) # sends the embed we just made
    else:
        # variables to declare
        author = ctx.author
        # embed
        userinfoEmbed = discord.Embed(title=f"{userinfo.name}", description="information we've received!") # creating an embed for the userinfo command 
        userinfoEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed 
        userinfoEmbed.set_thumbnail(url=userinfo.avatar_url) # adding an thumbnail to the embed
        userinfoEmbed.add_field(name="name", value=f"{userinfo.name}#{userinfo.discriminator}", inline = False) # adding a field to the embed
        userinfoEmbed.add_field(name="nickname", value=f"{userinfo.nick}", inline = False) # adding a field to the embed
        userinfoEmbed.add_field(name="id", value=f"{userinfo.id}", inline = False) # adding a field to the embed 
        userinfoEmbed.add_field(name="account creation", value=f"{userinfo.created_at}", inline = False) # adding a field to the embed
        # sends content
        await ctx.send(embed=userinfoEmbed) # sends the embed we just made

@client.command()
async def serverinfo(ctx):
    # variables to declare
    author = ctx.author
    serverName = ctx.guild.name
    owner = ctx.guild.owner
    serverId = ctx.guild.id
    icon = ctx.guild.icon_url
    memberCount = ctx.guild.member_count
    roleCount = len(ctx.guild.roles)
    region = ctx.guild.region
    # embed
    serverinfoEmbed = discord.Embed(title=f"{serverName}", description="information we've received!") # creating an embed for the serverinfo command 
    serverinfoEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed 
    serverinfoEmbed.set_thumbnail(url=icon) # adding a thumbnail to the embed
    serverinfoEmbed.add_field(name="owner", value=f"{owner.name}#{owner.discriminator}", inline = False) # adding a field to the embed
    serverinfoEmbed.add_field(name="sever id", value=f"{serverId}", inline = False) # adding a field to the embed
    serverinfoEmbed.add_field(name="member count", value=f"{memberCount}", inline = False) # adding a field to the embed
    serverinfoEmbed.add_field(name ="server region", value=f"{region}", inline = False) # adding a field to the embed
    serverinfoEmbed.add_field(name="role count", value=f"{roleCount}", inline = False) # adding a field to the embed
    # sends content
    await ctx.channel.send(embed=serverinfoEmbed) # sends the embed we just made

@client.command()
async def botinfo(ctx):
    # variables to declare 
    author = ctx.author
    bot = client.user
    botId = client.user.id
    botIcon = client.user.avatar_url
    botAge = client.user.created_at
    # embed 
    botinfoEmbed = discord.Embed(title=f"{bot.name}#{bot.discriminator}", description="information we've recieved!") # creating an embed for the botinfo command 
    botinfoEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed 
    botinfoEmbed.set_thumbnail(url=botIcon) # adding a thumbnail to the embed
    botinfoEmbed.add_field(name="name", value=f"{bot.name}#{bot.discriminator}", inline = False) # adding a field to the embed
    botinfoEmbed.add_field(name="id", value=f"{botId}", inline = False) # adding a field to the embed
    botinfoEmbed.add_field(name="bot creator", value="noicenoicebaby#0001", inline = False) # adding a field to the embed
    botinfoEmbed.add_field(name="bot creation", value=f"{botAge}", inline = False) # adding a field to the embed
    # sends content
    await ctx.channel.send(embed=botinfoEmbed) # sends the embed we just made

@client.command()
async def snipe(ctx):
    try:
        # variables to declare
        image_proxy_url, contents,author, channel_name, time = client.sniped_messages[ctx.guild.id] 
    except:
        # variables to declare 
        contents,author, channel_name, time = client.sniped_messages[ctx.guild.id]
    try:
        # image embed 
        snipeEmbed = discord.Embed(description=contents, timestamp=time) # creating an embed for the snipe command
        snipeEmbed.set_image(url=image_proxy_url) # adding an image to the embed
        snipeEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed 
        snipeEmbed.set_footer(text=f"Deleted in : #{channel_name}") # adding a footer to the embed
        # sends content
        await ctx.channel.send(embed=snipeEmbed) # sends the embed we just made 
    except:
        # embed
        snipeEmbed = discord.Embed(description=contents, timestamp=time) # creating an embed for the snipe command
        snipeEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed 
        snipeEmbed.set_footer(text=f"Deleted in : #{channel_name}") # adding a footer to the embed 
        # sends content
        await ctx.channel.send(embed=snipeEmbed) # sends the embed we just made 

@client.command(aliases=["doge"])
async def dog(ctx):
    # variables to declare 
    author = ctx.author
    dogImage = await dogApi.get(apiKey, random.choice(["jpg", "png", "gif"]))
    # embed
    dogEmbed = discord.Embed(title="dog") # creating an embed for the dog command 
    dogEmbed.set_image(url=dogImage) # adding an image to the embed
    dogEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed
    # sends content 
    await ctx.channel.send(embed=dogEmbed) # sends the embed we just made 

@client.command()
async def cat(ctx):
    # variables to declare 
    author = ctx.author
    catImage = await catApi.get(apiKey, random.choice(["jpg", "png", "gif"]))
    # embed
    catEmbed = discord.Embed(title="cat") # creating an embed for the cat command 
    catEmbed.set_image(url=catImage) # adding an image to the embed
    catEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed
    # sends content 
    await ctx.channel.send(embed=catEmbed) # sends the embed we just made 

@client.command()
async def github(ctx):
    # variables to declare 
    author = ctx.author
    bot = client.user
    botIcon = client.user.avatar_url
    # embed 
    githubEmbed = discord.Embed(title=f"source code for {bot.name}#{bot.discriminator}") # creating an embed for the github command
    githubEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed
    githubEmbed.set_thumbnail(url=botIcon) # adding a thumbnail to the embed
    githubEmbed.add_field(name="source code", value="https://github.com/NoiceNoiceBaby/noicebot") # adding a field to the embed
    # sends content
    await ctx.channel.send(embed=githubEmbed) # sends the embed we just made

# running the bot 
client.run(token) # client runs the token