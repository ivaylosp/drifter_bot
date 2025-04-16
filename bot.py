# bot.py
import os
import discord
import logging
import sys
import json

from dotenv import load_dotenv
from discord.ext import commands
from modules import drifter_scouts
from modules import mercenary_dens

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
CHANNEL_ROTATION = os.getenv('CHANNEL_ROTATION')

# Specifying supported intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
intents.guild_messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

#Booting up logger instance
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.command(help='Register drifter wormhole or mercenary den within the specialized channel')
async def add(ctx, *arguments):
    match ctx.message.channel.name:
        case drifter_scouts.channel:
            system = ""
            wormhole_type = ""
            eol = ""

            for index, value in enumerate(arguments):
                match (index):
                    case 0: system = value
                    case 1: wormhole_type = value
                    case 2: eol = value
                    case _:
                        print(f"Unsupported index with value {value}")
           
            await drifter_scouts.register_wormhole(ctx, system, wormhole_type, eol)
        case mercenary_dens.channel:
            
            system = ""
            planet_number = 0
            reinforcement_time = ""
            owner = ""

            for index, value in enumerate(arguments):
                match (index):
                    case 0: system = value
                    case 1: planet_number = value
                    case 2: reinforcement_time = value
                    case 3: owner = value
                    case _:
                        print(f"Unsupported index with value {value}")
            
            await mercenary_dens.register_mercenary_den(ctx, system, planet_number, reinforcement_time, owner)
        case _:
            return

@bot.command(help='Remove drifter wormhole or mercenary den from the database')
async def remove(ctx, *arguments):
    match ctx.message.channel.name:
        case drifter_scouts.channel:
            system = ""
            wormhole_type = ""

            for index, value in enumerate(arguments):
                match (index):
                    case 0: system = value
                    case 1: wormhole_type = value
                    case _:
                        print("Unsupported index with value {value}")

            await drifter_scouts.remove(ctx, system, wormhole_type)
        case mercenary_dens.channel:
            
            system = ""
            planet_number = 0

            for index, value in enumerate(arguments):
                match (index):
                    case 0: system = value
                    case 1: planet_number = value
                    case _:
                        print("Unsupported index with value {value}")

            await mercenary_dens.clear_mercenary_den(ctx, system, planet_number)
        case _:
            return

@bot.command(help='List all drifter wormholes or mercenary dens for a region with Paragon Soul as default')
async def list(ctx, *arguments):

    region = ''
    alliance_only = False

    for index, value in enumerate(arguments):
        if (index == 1 and value == "1"):
            alliance_only = True
        else:
            region += ' ' + value

    region = region.strip()

    match ctx.message.channel.name:
        case drifter_scouts.channel:
            await drifter_scouts.region_wormholes(ctx, region)
        case mercenary_dens.channel:
            await mercenary_dens.region_dens(ctx, region, alliance_only=alliance_only)
        case _:
            return

@bot.command(help='List all reinforced mercenary dens')
async def reffed(ctx):
    match ctx.message.channel.name:
        case mercenary_dens.channel:
            await mercenary_dens.region_dens(ctx, None, True)
        case _:
            return

@bot.command(help='Lists all supported regions')
async def regions(ctx):
    match ctx.message.channel.name:
        case drifter_scouts.channel:
            await drifter_scouts.list_regions(ctx)
        case mercenary_dens.channel:
            await mercenary_dens.list_regions(ctx)
        case _:
            return

@bot.command(help='Search for systems with specific wormhole type')
async def search(ctx, wormholeType:str=""):
    match ctx.message.channel.name:
        case drifter_scouts.channel:
            await drifter_scouts.search(ctx, wormholeType)
        case _:
            return

@bot.command(help='Alias for search')
async def find(ctx, wormholeType:str=""):
    match ctx.message.channel.name:
        case drifter_scouts.channel:
            await drifter_scouts.search(ctx, wormholeType)
        case _:
            return

@bot.event
async def on_ready():
    try:
        data = json.loads(CHANNEL_ROTATION)
        for rotation_settings in data:
            if os.path.exists(os.path.join("modules", rotation_settings['module'], "cog.py")):
                logger.info('Loading module %s!', rotation_settings['module'])
                bot.load_extension(f"modules.{rotation_settings['module']}.cog")
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON format: %s", e)

try:
    bot.run(TOKEN)
except:
    print('Something went wrong!')
