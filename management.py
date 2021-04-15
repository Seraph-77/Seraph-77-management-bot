#main discord function----------------
import discord
#additional installs------------------
from discord.utils import get
from discord.ext import commands
from discord.utils import find
#built-in to python requirements------
import random
import os
import youtube_dl


#required assets and how to install
#   python 3.9 : https://www.python.org/downloads/S
#   discord.py : https://pypi.org/project/discord.py/
#   youtube_dl : https://youtube-dl.org/
#   ffmpeg     : https://ffmpeg.org/
#
#   Lastly, you need an IDE(Integrated Development Environment)
#   I like to use Visual Studio Code, but some people use others
#   
#   Visual Studio Code : https://code.visualstudio.com/?wt.mc_id=DX_841432 


#prefix
client = commands.Bot (command_prefix = '~')
client.remove_command('help')

@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Thank you for adding me!. for questions or concerns, contact <@758025193980559402> {}!'.format(guild.name))

#bot startup
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('----------')
    print('Version 2.0.0')
    print('bot is active')
    print('----------')
    await client.change_presence(activity=discord.Game('Terminal'))

#error logging
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed=discord.Embed(title="Error : Missing Argument", description=":no_entry_sign: This command could not be ran, as you are missing a required argument", color=0xff0000)
        await ctx.send(embed=embed) 
    if isinstance(error, commands.MissingPermissions):
        embed=discord.Embed(title="Error : Missing permission", description=":no_entry_sign: This command could not be ran, as you are missing the permission to do so", color=0xff0000)
        await ctx.send(embed=embed)

#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------

@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        color = discord.Colour.dark_magenta()
    )
    
    embed.set_author(name='Seraph-77s help embed')
    embed.add_field(name="~unmute", value="unmutes a person. they can speak again(**admin only**)", inline=False)
    embed.add_field(name="~kick", value="kicks a member from the server.be sure to mention them after the 'kick' part. (**admin only**)", inline=False)
    embed.add_field(name="~ban", value="bans a member. same formatting as ~kick (**admin only**)", inline=False)
    embed.add_field(name="~8ball", value="ask 8ball a question! they will respond", inline=False)
    embed.add_field(name="~join", value="makes the bot join the current VC", inline=False)
    embed.add_field(name="~leave", value="bot leaves the VC", inline=False)
    embed.add_field(name="~debug", value="simulates an error to check if error logging works correctly", inline=False)
    embed.add_field(name="~play", value="plays a song ( **YOU NEED TO LINK A YT LINK AFTER '~play' FOR IT TO WORK**)", inline=True)
    embed.add_field(name="~cq", value="issue this command after every song. it clears the mp3 file that was saved from the previous use", inline=True)
    embed.set_footer(text="discord embed sandbox : https://cog-creators.github.io/discord-embed-sandbox/")
    await ctx.send(embed=embed)

#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------


#commands
@client.command()
async def ping(ctx):
    await ctx.send(f'Latency :  {round(client.latency * 1000)}ms')

@client.command()
async def debug(ctx):
    embed=discord.Embed(title="Error : Missing Argument", description=":no_entry_sign: This command could not be ran, as you are missing a required argument", color=0xff0000)
    await ctx.send(embed=embed)
    embed=discord.Embed(title="Error : Missing permission", description=":no_entry_sign: This command could not be ran, as you are missing the permission to do so", color=0xff0000)
    await ctx.send(embed=embed)

    

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)


@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, reason: str = None):
    muted = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(muted)
    channel = client.get_channel(832224954930036746)
    await channel.send(f' :no_entry_sign: muted {member}')

@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member, reason: str = None):
    muted = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(muted)
    channel = client.get_channel(832224954930036746)
    await channel.send(f' :white_check_mark: un-muted {member}'))


@client.command()
@commands.has_permissions(manage_messages=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    channel = client.get_channel(832224954930036746)
    await channel.send(f'kicked {member} for {reason}')

@client.command()
@commands.has_permissions(manage_messages=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    channel = client.get_channel(832224954930036746)
    await channel.send(f'banned {member} for {reason}')

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = [
                 'It is certain.',
                 'It is decidedly so.',
                 'Without a doubt.',
                 'Yes - definitely.',
                 'You may rely on it.',
                 'As I see it, yes.',
                 'Most likely.',
                 'Outlook good.',
                 'Yes.',
                 'Signs point to yes.',
                 'Reply hazy, try again.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 'Dont count on it.',
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                'Very doubtful.'  ]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------

#music commands
@client.command()
async def cq(ctx):
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            await ctx.send('clearing songs')
            os.remove("song.mp3")

@client.command(pass_context=True)
async def join(ctx):
    if ctx.message.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()

@client.command(pass_context=True)
async def leave(ctx):
    if ctx.message.author.voice:
        
        channel = ctx.message.guild.voice_client
        await channel.disconnect()

@client.command(pass_context=True)
async def play(ctx, url):
 
    try:
        if os._exists("song.mp3"):
            os.remove("song.mp3")
    except PermissionError:
        await ctx.message.channel.send("Music is playing right now! Use ~stop to stop it.")
 
    voice = get(client.voice_clients,guild=ctx.guild)
    ydl_options={
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key':'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '150'
        }],
 
    }
 
    with youtube_dl.YoutubeDL(ydl_options) as ydl:
        await ctx.message.channel.send("Loading music...")
        try:
            ydl.download([url])
        except:
            await ctx.message.channel.send("Error in loading music!")
            return
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            print(f"Renaming file : {file}")
            os.rename(file, "song.mp3")


            
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.1

#YTDL Options
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
 
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

client.run('ODAzNDA3NDEyMjYxNTUyMTM4.YA9VdQ.mXEtKKHRDvZJg4YgBdhYWLefhxk')
