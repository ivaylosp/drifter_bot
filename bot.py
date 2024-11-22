# bot.py
import os
import discord
import logging
import sys

from dotenv import load_dotenv
from discord.ext import commands
from modules import drifter_scouts
from modules import mercenary_dens

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Specifying supported intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
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
                        print("Unsupported index with value {value}")
           
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
                        print("Unsupported index with value {value}")
            
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
async def list(ctx, region:str='Paragon Soul', alliance_only:int=0):
    match ctx.message.channel.name:
        case drifter_scouts.channel:
            await drifter_scouts.region_wormholes(ctx, region)
        case mercenary_dens.channel:
            alliance_only = True if alliance_only == 1 else False
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

try:
    bot.run(TOKEN)
except:
    print(f"Something went wrong!")
