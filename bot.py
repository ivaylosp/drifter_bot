# bot.py
import os
import discord
import hashlib
import json

from os.path import exists
from collections.abc import Iterable
from dotenv import load_dotenv
from discord.ext import commands
from enum import Enum

class DrifterWormholeTypes(Enum):
    V = 'Vidette V928'
    R = 'Redoubt R259'
    S = 'Sentinel S877'
    B = 'Barbican B735'
    C = 'Conflux C414'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('DISCORD_CHANNEL')

# Specifying supported intents
intents = discord.Intents.default()
intents.message_content = True

# Storage
storage = [
    {'region' : 'Catch', 'system':'25S-6P', 'wormholes':[]},
    {'region' : 'Catch', 'system':'3GD6-8', 'wormholes':[]},
    {'region' : 'Catch', 'system':'4-07MU', 'wormholes':[]},
    {'region' : 'Catch', 'system':'7LHB-Z', 'wormholes':[]},
    {'region' : 'Catch', 'system':'9-8GBA', 'wormholes':[]},
    {'region' : 'Catch', 'system':'AX-DOT', 'wormholes':[]},
    {'region' : 'Catch', 'system':'B-XJX4', 'wormholes':[]},
    {'region' : 'Catch', 'system':'E3-SDZ', 'wormholes':[]},
    {'region' : 'Catch', 'system':'EX-0LQ', 'wormholes':[]},
    {'region' : 'Catch', 'system':'F4R2-Q', 'wormholes':[]},
    {'region' : 'Catch', 'system':'F9E-KX', 'wormholes':[]},
    {'region' : 'Catch', 'system':'G-AOTH', 'wormholes':[]},
    {'region' : 'Catch', 'system':'GE-94X', 'wormholes':[]},
    {'region' : 'Catch', 'system':'I-8D0G', 'wormholes':[]},
    {'region' : 'Catch', 'system':'IS-R7P', 'wormholes':[]},
    {'region' : 'Catch', 'system':'JA-O6J', 'wormholes':[]},
    {'region' : 'Catch', 'system':'JWZ2-V', 'wormholes':[]},
    {'region' : 'Catch', 'system':'L7XS-5', 'wormholes':[]},
    {'region' : 'Catch', 'system':'OGL8-Q', 'wormholes':[]},
    {'region' : 'Catch', 'system':'SNFV-I', 'wormholes':[]},
    {'region' : 'Catch', 'system':'ZQ-Z3Y', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'15U-JY', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'6F-H3W', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'7BX-6F', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'7X-02R', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'87XQ-0', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'A-HZYL', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'AC2E-3', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'CHA2-Q', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'G-UTHL', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'H-S80W', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'HMF-9D', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'I-CUVX', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'IGE-RI', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'JGOW-Y', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'KCT-0A', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'L-1SW8', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'P5-EFH', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'PXF-RF', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'Q-XEB3', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'R3W-XU', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'SPLE-Y', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'UAYL-F', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'V6-NY1', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'YRNJ-8', 'wormholes':[]},
    {'region' : 'Fountain', 'system':'Z-YN5Y', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'0MV-4W', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'1N-FJ8', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'1VK-6B', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'1W-0KS', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'5T-KM3', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'6WW-28', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'7-K5EL', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'BR-6XP', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'FS-RFL', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'H-NOU5', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'JZV-F4', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'LS9B-9', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'MGAM-4', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'MQ-O27', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'O-LR1H', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'P3EN-E', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'Q-R3GP', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'S-NJBB', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'VI2K-J', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'XSQ-TF', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'Z-8Q65', 'wormholes':[]},
    {'region' : 'Vale_of_the_Silent', 'system':'ZA0L-U', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'6-I162', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'AC-7LZ', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'CJNF-J', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'FRTC-5', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'NS2L-4', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'O7-7UX', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'R-ORB7', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'U9U-TQ', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'Y-C4AL', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'Y-FZ5N', 'wormholes':[]},
    {'region' : 'Immensea', 'system':'Y19P-1', 'wormholes':[]},
    {'region' : 'Providence', 'system':'2V-CS5', 'wormholes':[]},
    {'region' : 'Providence', 'system':'8P9-BM', 'wormholes':[]},
    {'region' : 'Providence', 'system':'9UY4-H', 'wormholes':[]},
    {'region' : 'Providence', 'system':'D-6WS1', 'wormholes':[]},
    {'region' : 'Providence', 'system':'FSW-3C', 'wormholes':[]},
    {'region' : 'Providence', 'system':'GN7-XY', 'wormholes':[]},
    {'region' : 'Providence', 'system':'HP-6Z6', 'wormholes':[]},
    {'region' : 'Providence', 'system':'I-MGAB', 'wormholes':[]},
    {'region' : 'Providence', 'system':'K1Y-5H', 'wormholes':[]},
    {'region' : 'Providence', 'system':'MH9C-S', 'wormholes':[]},
    {'region' : 'Providence', 'system':'N-RMSH', 'wormholes':[]},
    {'region' : 'Providence', 'system':'OXIY-V', 'wormholes':[]},
    {'region' : 'Providence', 'system':'QBL-BV', 'wormholes':[]},
    {'region' : 'Providence', 'system':'QR-K85', 'wormholes':[]},
    {'region' : 'Providence', 'system':'TU-O0T', 'wormholes':[]},
    {'region' : 'Curse', 'system':'ES-UWY', 'wormholes':[]},
    {'region' : 'Curse', 'system':'G-G78S', 'wormholes':[]},
    {'region' : 'Curse', 'system':'J7A-UR', 'wormholes':[]},
    {'region' : 'Curse', 'system':'K-MGJ7', 'wormholes':[]},
    {'region' : 'Curse', 'system':'V7D-JD', 'wormholes':[]},
    {'region' : 'Curse', 'system':'Y-K50G', 'wormholes':[]},
    {'region' : 'Tribute', 'system':'C2X-M5', 'wormholes':[]},
    {'region' : 'Tribute', 'system':'C8VC-S', 'wormholes':[]},
    {'region' : 'Tribute', 'system':'F-749O', 'wormholes':[]},
    {'region' : 'Tribute', 'system':'NJ4X-S', 'wormholes':[]},
    {'region' : 'Tribute', 'system':'S8-NSQ', 'wormholes':[]},
    {'region' : 'Tribute', 'system':'SH1-6P', 'wormholes':[]},
    {'region' : 'Tribute', 'system':'V0DF-2', 'wormholes':[]},
    {'region' : 'Tribute', 'system':'W-UQA5', 'wormholes':[]},
    {'region' : 'Tribute', 'system':'WH-JCA', 'wormholes':[]},
    {'region' : 'Tribute', 'system':'XD-TOV', 'wormholes':[]},
    {'region' : 'Pure_Blind', 'system':'12YA-2', 'wormholes':[]},
    {'region' : 'Pure_Blind', 'system':'4-ABS8', 'wormholes':[]},
    {'region' : 'Pure_Blind', 'system':'5ZXX-K', 'wormholes':[]},
    {'region' : 'Pure_Blind', 'system':'JC-YX8', 'wormholes':[]},
    {'region' : 'Pure_Blind', 'system':'KQK1-2', 'wormholes':[]},
    {'region' : 'Pure_Blind', 'system':'R-2R0G', 'wormholes':[]},
    {'region' : 'Pure_Blind', 'system':'RORZ-H', 'wormholes':[]},
    {'region' : 'Pure_Blind', 'system':'RZC-16', 'wormholes':[]},
    {'region' : 'Pure_Blind', 'system':'S-MDYI', 'wormholes':[]},
    {'region' : 'Pure_Blind', 'system':'U-INPD', 'wormholes':[]},
    {'region' : 'Pure_Blind', 'system':'UC3H-Y', 'wormholes':[]},
    {'region' : 'Pure_Blind', 'system':'UI-8ZE', 'wormholes':[]},
    {'region' : 'Pure_Blind', 'system':'WW-KGD', 'wormholes':[]},
    {'region' : 'Etherium_Reach', 'system':'1PF-BC', 'wormholes':[]},
    {'region' : 'Etherium_Reach', 'system':'3IK-7O', 'wormholes':[]},
    {'region' : 'Etherium_Reach', 'system':'4-QDIX', 'wormholes':[]},
    {'region' : 'Etherium_Reach', 'system':'89-JPE', 'wormholes':[]},
    {'region' : 'Etherium_Reach', 'system':'8KE-YS', 'wormholes':[]},
    {'region' : 'Etherium_Reach', 'system':'9P-870', 'wormholes':[]},
    {'region' : 'Etherium_Reach', 'system':'CT8K-0', 'wormholes':[]},
    {'region' : 'Etherium_Reach', 'system':'F69O-M', 'wormholes':[]},
    {'region' : 'Etherium_Reach', 'system':'IRD-HU', 'wormholes':[]},
    {'region' : 'Etherium_Reach', 'system':'KGT3-6', 'wormholes':[]},
    {'region' : 'Etherium_Reach', 'system':'KMH-J1', 'wormholes':[]},
    {'region' : 'Etherium_Reach', 'system':'RO-0PZ', 'wormholes':[]},
    {'region' : 'Etherium_Reach', 'system':'WPV-JN', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'0-U2M4', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'4-1ECP', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'9-ZA4Z', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'A1F-22', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'BEG-RL', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'E-WMT7', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'H-29TM', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'J9A-BH', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'JPEZ-R', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'JZ-UQC', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'LW-YEW', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'M4-KX5', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'MJ-5F9', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'MTO2-2', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'O-QKSM', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'OP7-BP', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'PE-SAM', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'PFV-ZH', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'RY-2FX', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'SY-OLX', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'TAL1-3', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'VWES-Y', 'wormholes':[]},
    {'region' : 'Perrigen_Falls', 'system':'XU7-CH', 'wormholes':[]},
    {'region' : 'Delve', 'system':'8F-TK3', 'wormholes':[]},
    {'region' : 'Delve', 'system':'D-W7F0', 'wormholes':[]},
    {'region' : 'Delve', 'system':'F-9PXR', 'wormholes':[]},
    {'region' : 'Delve', 'system':'HM-XR2', 'wormholes':[]},
    {'region' : 'Delve', 'system':'IP6V-X', 'wormholes':[]},
    {'region' : 'Delve', 'system':'KBAK-I', 'wormholes':[]},
    {'region' : 'Delve', 'system':'M-SRKS', 'wormholes':[]},
    {'region' : 'Delve', 'system':'QY6-RK', 'wormholes':[]},
    {'region' : 'Delve', 'system':'YZ9-F6', 'wormholes':[]},
    {'region' : 'Delve', 'system':'Z3V-1W', 'wormholes':[]},
    {'region' : 'Delve', 'system':'ZXB-VC', 'wormholes':[]},
]
# perrigan falls
dotlanUrl = 'https://evemaps.dotlan.net/map/'

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

file_exists = exists('database.json')

if (file_exists):
    with open("database.json") as file:
        storage = json.load(file)

@bot.command(help='Register new drifter wormhole to the database')
async def add(ctx, system: str, wormholeType: str):
    if CHANNEL not in ctx.message.channel.name: return

    try:
        drifterWormholeDesignation = DrifterWormholeTypes[wormholeType].value
        wormholeType = wormholeType.capitalize()

        for region in storage:
            if (region['system'] == system):
                wormholes = region['wormholes']
                region['wormholes'] += [wormholeType]
                payload = region['system'] + '    >>    ' + drifterWormholeDesignation

        ## Persist data into a file
        with open("database.json", 'w') as file:
            json.dump(storage, file)

        await ctx.send(payload)
    except KeyError as exception:
        await ctx.send(f"""
You entered `{wormhole_type}`, which is not a valid drifter wormhole identifier.
```
Supported identifiers:

V - Vidette V928
R - Redoubt R259
S - Sentinel S877
B - Barbican B735
C - Conflux C414
```""")

@bot.command(help='Remove a drifter wormhole from the database')
async def remove(ctx, system: str, wormholeType: str):
    if CHANNEL not in ctx.message.channel.name: return

    try:
        drifterWormholeDesignation = DrifterWormholeTypes[wormholeType].value
        wormholeType = wormholeType.capitalize()
        payload = 'Could not find drifter type ' + wormholeType + ' in ' + system

        for region in storage:
            if (region['system'] == system):
                wormholes = region['wormholes']
                for index, wormhole in enumerate(wormholes):
                    if (wormhole == wormholeType):
                        wormholes.pop(index)
                        region['wormholes'] = wormholes
                        payload = region['system'] + '    REMOVED    ' + drifterWormholeDesignation\

        ## Persist data into a file
        with open("database.json", 'w') as file:
            json.dump(storage, file)

        await ctx.send(payload)
    except KeyError as exception:
        await ctx.send(f"""
You entered `{wormhole_type}`, which is not a valid drifter wormhole identifier.
```
Supported identifiers:

V - Vidette V928
R - Redoubt R259
S - Sentinel S877
B - Barbican B735
C - Conflux C414
```""")

@bot.command(help='List all drifter wormholes for a region with Catch as default')
async def list(ctx, region:str='Catch'):
    if CHANNEL not in ctx.message.channel.name: return

    region = region.title().replace(" ","_")
    url = dotlanUrl + region.replace(" ", "_") + '/'

    payload = '```[' + region + ']' + os.linesep + os.linesep

    for wormhole in storage:
        if (region == wormhole['region']):
            wormholes = wormhole['wormholes']
            if isinstance(wormholes, Iterable):
                wormholes = ' '.join(wormholes)
            else:
                wormholes = ''
            payload += wormhole['system'] + '    >>    ' + wormholes + os.linesep
            url += wormhole['system'] + ','

    payload += '```'
    payload += '<' + url[:-1] + '>'
    await ctx.send(payload)

@bot.command(help='Initialize datastore')
async def init(ctx, password:str):
    if CHANNEL not in ctx.message.channel.name: return

    env_password = os.getenv('ADMIN_PASSWORD')
    if (env_password == password):
        with open("database.json", 'w') as file:
            json.dump(storage, file)

@bot.command(help='Lists all supported regions')
async def regions(ctx):
    if CHANNEL not in ctx.message.channel.name: return

    regions = []
    payload = '```[Regions]' + os.linesep + os.linesep

    for region in storage:
        if region['region'] not in regions:
            regions.append(region['region'])
            payload += region['region'] + os.linesep

    payload += '```'
    await ctx.send(payload)

try:
    bot.run(TOKEN)
except:
    print(f"Something went wrong!")